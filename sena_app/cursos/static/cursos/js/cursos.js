// Lógica de filtrado, búsqueda y ordenamiento para Cursos (alineada a Programas)
(function(){
  const q = (sel) => document.querySelector(sel);
  const qa = (sel) => Array.from(document.querySelectorAll(sel));

  const searchInput = q('#cursoSearch');
  const programaFilter = q('#cursoFiltroPrograma');
  const coordinadorFilter = q('#cursoFiltroCoordinador');
  const estadoFilter = q('#cursoFiltroEstado');
  const table = q('#tablaCursos');
  const sortButtons = table ? table.querySelectorAll('button.table-sort') : [];
  if(!table) return;

  // Poblar filtros con valores únicos presentes en la tabla (si los selects existen)
  (function populateFilters(){
    const rows = qa('#tablaCursos tbody tr');
    const programas = new Set();
    const coordinadores = new Set();
    const estados = new Set();

    rows.forEach(tr => {
      const progAttr = (tr.getAttribute('data-programa') || '').trim();
      const coordAttr = (tr.getAttribute('data-coordinador') || '').trim();
      const estadoAttr = (tr.getAttribute('data-estado') || '').trim();
      if(progAttr) programas.add(progAttr);
      if(coordAttr) coordinadores.add(coordAttr);
      if(estadoAttr) estados.add(estadoAttr);
    });

    function ensureOptions(selectEl, values){
      if(!selectEl) return;
      // normalizar existentes a minúsculas para comparar sin duplicar
      const existingLower = Array.from(selectEl.querySelectorAll('option')).map(o => (o.value || '').toLowerCase());
      const toAdd = Array.from(values).filter(v => v && !existingLower.includes(v.toLowerCase()));
      toAdd.sort().forEach(v => {
        const opt = document.createElement('option');
        opt.value = v.toLowerCase();
        opt.textContent = v;
        selectEl.appendChild(opt);
      });
      // deduplicación defensiva por si hubiera repetidos en el DOM
      const seen = new Set();
      for(let i = selectEl.options.length - 1; i >= 0; i--){
        const val = (selectEl.options[i].value || '').toLowerCase();
        if(seen.has(val)){
          selectEl.remove(i);
        } else {
          seen.add(val);
        }
      }
    }

    ensureOptions(programaFilter, programas);
    ensureOptions(coordinadorFilter, coordinadores);
    ensureOptions(estadoFilter, estados);
  })();

  let sortState = {};

  function filtrar(){
    const txt = (searchInput?.value || '').trim().toLowerCase();
    const prog = (programaFilter?.value || '').trim().toLowerCase();
    const coord = (coordinadorFilter?.value || '').trim().toLowerCase();
    const estado = (estadoFilter?.value || '').trim().toLowerCase();

    let visibles = 0;
    qa('#tablaCursos tbody tr').forEach(tr => {
      const codigo = (tr.children[0]?.textContent || '').toLowerCase();
      const nombre = (tr.children[1]?.textContent || '').toLowerCase();
      const programaTxt = (tr.children[2]?.textContent || '').toLowerCase();
      const coordinadorTxt = (tr.children[3]?.textContent || '').toLowerCase();
      const estadoTxt = (tr.children[4]?.textContent || '').toLowerCase();
      const programaAttr = (tr.getAttribute('data-programa') || '').toLowerCase();
      const coordinadorAttr = (tr.getAttribute('data-coordinador') || '').toLowerCase();
      const estadoAttr = (tr.getAttribute('data-estado') || '').toLowerCase();

      let visible = true;
      if(txt){
        visible = codigo.includes(txt) || nombre.includes(txt) || programaTxt.includes(txt) || coordinadorTxt.includes(txt) || estadoTxt.includes(txt);
      }
      if(visible && prog){ visible = programaAttr === prog || programaTxt === prog; }
      if(visible && coord){ visible = coordinadorAttr === coord || coordinadorTxt === coord; }
      if(visible && estado){ visible = estadoAttr === estado || estadoTxt === estado; }

      tr.style.display = visible ? '' : 'none';
      if(visible) visibles++;
    });

    const badge = document.querySelector('[data-role="cursos-total"]');
    if(badge){ badge.textContent = `Cursos: ${visibles}`; }
  }

  function sortTable(colIndex){
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr')).filter(tr => tr.style.display !== 'none');
    const current = sortState[colIndex] || 'desc';
    const nextDir = current === 'asc' ? 'desc' : 'asc';
    sortState[colIndex] = nextDir;

    rows.sort((a,b)=>{
      const aText = (a.children[colIndex]?.textContent || '').trim().toLowerCase();
      const bText = (b.children[colIndex]?.textContent || '').trim().toLowerCase();
      const aNum = Number(aText);
      const bNum = Number(bText);
      if(!Number.isNaN(aNum) && !Number.isNaN(bNum)){
        return nextDir === 'asc' ? (aNum - bNum) : (bNum - aNum);
      }
      if(aText < bText) return nextDir === 'asc' ? -1 : 1;
      if(aText > bText) return nextDir === 'asc' ? 1 : -1;
      return 0;
    });

    rows.forEach(r=>tbody.appendChild(r));
  }

  // Eventos
  [searchInput, programaFilter, coordinadorFilter, estadoFilter].forEach(el=>{
    if(!el) return;
    el.addEventListener('input', filtrar);
    el.addEventListener('change', filtrar);
  });

  sortButtons.forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const col = parseInt(btn.getAttribute('data-col'), 10);
      sortTable(col);
    });
  });

  // Botón de refresco (opcional)
  q('#refreshCursos')?.addEventListener('click', ()=>{
    if(searchInput) searchInput.value='';
    if(programaFilter) programaFilter.value='';
    if(coordinadorFilter) coordinadorFilter.value='';
    if(estadoFilter) estadoFilter.value='';
    filtrar();
  });

  // Inicial
  filtrar();
})();
