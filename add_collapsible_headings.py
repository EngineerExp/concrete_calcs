

"""
Script to add collapsible headings to an exported Jupyter HTML file.
Usage:
    python add_collapsible_headings.py input.html output.html [--collapse-by-default]
This will read input.html, inject JavaScript for collapsible headings, and write to output.html.
The optional flag --collapse-by-default starts sections collapsed.
"""
import sys
import os


def inject_collapsible_js(html_content, collapse_by_default=False):
    """Return html_content with injected CSS+JS that makes headings collapsible.

    collapse_by_default: when True, sections start collapsed.
    """
    js_code = '''<style>
.collapsible-toggle {
  display: inline-block;
  width: 1.2em;
  text-align: center;
  margin-right: 0.4em;
  font-weight: bold;
  user-select: none;
}
.collapsible-toggle:focus { outline: 2px solid #5B9DD9; outline-offset: 2px; }
.collapsible-wrapper {
  margin: 0 0 0 0.8em;
}
.collapsible-heading { cursor: pointer; }
</style>
<script>
// Defer execution until DOM is ready
function __cc_init_collapsible(){
  // helper
  function levelOf(h){ return parseInt(h.tagName.substring(1),10); }
  const collapseByDefault = <<COLLAPSE_FLAG>>;

  // insert expand/collapse-all controls near top of document
  function insertGlobalToolbar(){
    try{
      const container = document.querySelector('main') || document.body;
      const bar = document.createElement('div');
      bar.style.margin = '0 0 1em 0';
      bar.style.display = 'flex';
      bar.style.gap = '0.5em';

      const expandAll = document.createElement('button');
      expandAll.textContent = 'Expand all';
      expandAll.setAttribute('type','button');
      expandAll.className = 'cc-expand-all';

      const collapseAll = document.createElement('button');
      collapseAll.textContent = 'Collapse all';
      collapseAll.setAttribute('type','button');
      collapseAll.className = 'cc-collapse-all';

      bar.appendChild(expandAll);
      bar.appendChild(collapseAll);
      container.insertBefore(bar, container.firstChild);

      expandAll.addEventListener('click', ()=>{
        document.querySelectorAll('.collapsible-wrapper').forEach(w=>{ w.style.display = ''; });
        document.querySelectorAll('.collapsible-toggle').forEach(t=> t.setAttribute('aria-expanded','true'));
        document.querySelectorAll('.collapsible-heading').forEach(h=> h.setAttribute('aria-expanded','true'));
      });
      collapseAll.addEventListener('click', ()=>{
        document.querySelectorAll('.collapsible-wrapper').forEach(w=>{ w.style.display = 'none'; });
        document.querySelectorAll('.collapsible-toggle').forEach(t=> t.setAttribute('aria-expanded','false'));
        document.querySelectorAll('.collapsible-heading').forEach(h=> h.setAttribute('aria-expanded','false'));
      });
    }catch(e){ /* non-fatal */ }
  }

  insertGlobalToolbar();

  // find headings in order
  const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'));
  headings.forEach((heading)=>{
    const myLevel = levelOf(heading);

    // locate enclosing cell (.jp-Cell) if present
    let mdCell = heading.closest ? heading.closest('.jp-Cell') : null;
    if(!mdCell){
      let p = heading.parentElement;
      while(p && !p.classList.contains('jp-Cell')) p = p.parentElement;
      mdCell = p;
    }
    if(!mdCell) return;

    // build toggle
    const toggle = document.createElement('button');
    toggle.className = 'collapsible-toggle';
    toggle.setAttribute('aria-label','Toggle section');
    toggle.type = 'button';
    toggle.textContent = '▾';
    toggle.title = 'Toggle section';
    toggle.style.verticalAlign = 'middle';

    heading.classList.add('collapsible-heading');
    heading.setAttribute('tabindex','0');
    heading.insertBefore(toggle, heading.firstChild);

    // collect following cells until next heading of same/higher level
    const wrapper = document.createElement('div');
    wrapper.className = 'collapsible-wrapper';
    let sib = mdCell.nextElementSibling;
    while(sib){
      const innerH = sib.querySelector && sib.querySelector('h1,h2,h3,h4,h5,h6');
      if(innerH && levelOf(innerH) <= myLevel) break;
      const next = sib.nextElementSibling;
      wrapper.appendChild(sib);
      sib = next;
    }

    if(wrapper.childElementCount > 0){
      // give wrapper a unique id for aria-controls
      const wrapperId = 'collapsible-wrapper-' + Math.random().toString(36).slice(2,9);
      wrapper.id = wrapperId;
      mdCell.parentNode.insertBefore(wrapper, mdCell.nextElementSibling);

      const setCollapsed = (c)=>{
        wrapper.style.display = c ? 'none' : '';
        toggle.textContent = c ? '▸' : '▾';
        toggle.setAttribute('aria-expanded', String(!c));
        heading.setAttribute('aria-expanded', String(!c));
      };

      let collapsed = !!collapseByDefault;
      toggle.setAttribute('aria-expanded', String(!collapsed));
      heading.setAttribute('role','button');
      heading.setAttribute('aria-expanded', String(!collapsed));
      toggle.setAttribute('aria-controls', wrapperId);

      const clickHandler = (ev)=>{ if(ev.target.tagName === 'A') return; collapsed = !collapsed; setCollapsed(collapsed); ev.stopPropagation(); };
      toggle.addEventListener('click', clickHandler);
      heading.addEventListener('click', function(ev){ if(ev.target.tagName === 'A') return; clickHandler(ev); });

      // keyboard: Enter or Space toggles
      heading.addEventListener('keydown', function(ev){
        if(ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); clickHandler(ev); }
      });

      setCollapsed(collapsed);
    }
  });
}

if (document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', __cc_init_collapsible);
} else {
  __cc_init_collapsible();
}
</script>'''

    # inject the chosen collapse flag literal
    js_code = js_code.replace('<<COLLAPSE_FLAG>>', str(collapse_by_default).lower())

    if '</body>' in html_content:
        return html_content.replace('</body>', js_code + '\n</body>')
    else:
        return html_content + js_code


def main():
    # Accept optional flag --collapse-by-default as third argument
    if len(sys.argv) not in (3,4):
        print("Usage: python add_collapsible_headings.py input.html output.html [--collapse-by-default]")
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]
    collapse_flag = False
    if len(sys.argv) == 4:
        if sys.argv[3] == '--collapse-by-default':
            collapse_flag = True
        else:
            print(f"Unknown option: {sys.argv[3]}")
            sys.exit(2)
    if not os.path.isfile(input_path):
        print(f"Input file {input_path} does not exist.")
        sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    new_content = inject_collapsible_js(html_content, collapse_by_default=collapse_flag)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Collapsible headings added. Output written to {output_path}")


if __name__ == '__main__':
    main()
