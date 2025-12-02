(function(){
  const tabla = document.getElementById('tablaAprendices');
  if(!tabla) return;

  const searchInput = document.getElementById('aprendizSearch');
  const filtroPrograma = document.getElementById('filtroPrograma');
  const filtroCiudad = document.getElementById('filtroCiudad');

  const sortButtons = tabla.querySelectorAll('button.table-sort');
  let sortState = {};

  // Poblar selects con valores únicos
  (function populateFilters(){
    if(!filtroPrograma || !filtroCiudad) return;
    const programas = new Set();
    const ciudades = new Set();
    tabla.querySelectorAll('tbody tr').forEach(tr=>{
      const prog = tr.getAttribute('data-programa');
      const ciu = tr.getAttribute('data-ciudad');
      if(prog) programas.add(prog);
      if(ciu) ciudades.add(ciu);
    });
    [...programas].sort().forEach(p=>{
      const opt = document.createElement('option');
      opt.value = p; opt.textContent = p; filtroPrograma.appendChild(opt);
    });
    [...ciudades].sort().forEach(c=>{
      const opt = document.createElement('option');
      opt.value = c; opt.textContent = c; filtroCiudad.appendChild(opt);
    });
  })();

  function filtrar(){
    const txt = (searchInput?.value || '').toLowerCase().trim();
    const prog = (filtroPrograma?.value || '').toLowerCase();
    const ciu = (filtroCiudad?.value || '').toLowerCase();
    tabla.querySelectorAll('tbody tr').forEach(tr=>{
      const doc = tr.children[0].textContent.toLowerCase();
      const nombre = tr.children[1].textContent.toLowerCase();
      const apellido = tr.children[2].textContent.toLowerCase();
      const programa = (tr.getAttribute('data-programa')||'').toLowerCase();
      const ciudad = (tr.getAttribute('data-ciudad')||'').toLowerCase();
      let visible = true;
      if(txt){
        visible = doc.includes(txt) || nombre.includes(txt) || apellido.includes(txt) || programa.includes(txt);
      }
      if(visible && prog){ visible = programa === prog; }
      if(visible && ciu){ visible = ciudad === ciu; }
      tr.style.display = visible ? '' : 'none';
    });
  }

  [searchInput, filtroPrograma, filtroCiudad].forEach(el=>{
    if(!el) return;
    el.addEventListener('input', filtrar);
    el.addEventListener('change', filtrar);
  });

  function sortTable(colIndex){
    const tbody = tabla.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const current = sortState[colIndex] || 'desc';
    const nextDir = current === 'asc' ? 'desc' : 'asc';
    sortState[colIndex] = nextDir;
    rows.sort((a,b)=>{
      // Omite filas ocultas? mantiene orden igualmente
      const aText = a.children[colIndex].textContent.trim().toLowerCase();
      const bText = b.children[colIndex].textContent.trim().toLowerCase();
      if(!isNaN(aText) && !isNaN(bText)){
        return nextDir === 'asc' ? (+aText - +bText) : (+bText - +aText);
      }
      if(aText < bText) return nextDir === 'asc' ? -1 : 1;
      if(aText > bText) return nextDir === 'asc' ? 1 : -1;
      return 0;
    });
    rows.forEach(r=>tbody.appendChild(r));
  }

  sortButtons.forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const col = +btn.getAttribute('data-col');
      sortTable(col);
    });
  });
})();
