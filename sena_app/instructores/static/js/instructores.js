(function(){
  const searchInput = document.getElementById('instructorSearch');
  const filtroEspecialidad = document.getElementById('filtroEspecialidad');
  const filtroActivo = document.getElementById('filtroActivo');
  const filtroCiudad = document.getElementById('filtroCiudad');
  const tabla = document.getElementById('tablaInstructores');
  const sortButtons = tabla ? tabla.querySelectorAll('button.table-sort') : [];

  if(!tabla) return;

  // Poblar opciones únicas
  (function populate(){
    if(filtroEspecialidad){
      const especialidades = new Set();
      tabla.querySelectorAll('tbody tr').forEach(tr=>{
        const esp = tr.getAttribute('data-especialidad');
        if(esp) especialidades.add(esp);
      });
      [...especialidades].sort().forEach(esp=>{
        const opt = document.createElement('option');
        opt.value = esp; opt.textContent = esp; filtroEspecialidad.appendChild(opt);
      });
    }
    if(filtroCiudad){
      const ciudades = new Set();
      tabla.querySelectorAll('tbody tr').forEach(tr=>{
        const ciu = tr.getAttribute('data-ciudad');
        if(ciu) ciudades.add(ciu);
      });
      [...ciudades].sort().forEach(c=>{
        const opt = document.createElement('option');
        opt.value = c; opt.textContent = c; filtroCiudad.appendChild(opt);
      });
    }
  })();

  function filtrar(){
    const txt = (searchInput?.value || '').toLowerCase();
    const espFiltro = (filtroEspecialidad?.value || '').toLowerCase();
    const ciudadFiltro = (filtroCiudad?.value || '').toLowerCase();
    const activoFiltro = filtroActivo?.value || '';

    tabla.querySelectorAll('tbody tr').forEach(tr=>{
      const doc = tr.children[0].textContent.toLowerCase();
      const nombre = tr.children[1].textContent.toLowerCase();
      const apellido = tr.children[2].textContent.toLowerCase();
      const especialidad = tr.getAttribute('data-especialidad')?.toLowerCase() || '';
      const ciudad = tr.getAttribute('data-ciudad')?.toLowerCase() || '';
      const activo = tr.getAttribute('data-activo');
      let visible = true;
      if(txt){
        visible = doc.includes(txt) || nombre.includes(txt) || apellido.includes(txt) || especialidad.includes(txt) || ciudad.includes(txt);
      }
      if(visible && espFiltro){ visible = especialidad === espFiltro; }
      if(visible && ciudadFiltro){ visible = ciudad === ciudadFiltro; }
      if(visible && activoFiltro){ visible = activo === activoFiltro; }
      tr.style.display = visible ? '' : 'none';
    });
  }

  [searchInput, filtroEspecialidad, filtroCiudad, filtroActivo].forEach(el=>{
    el && el.addEventListener('input', filtrar);
    el && el.addEventListener('change', filtrar);
  });

  let sortState = {};
  function sortTable(colIndex){
    const tbody = tabla.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const current = sortState[colIndex] || 'desc';
    const nextDir = current === 'asc' ? 'desc' : 'asc';
    sortState[colIndex] = nextDir;
    rows.sort((a,b)=>{
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
      const col = parseInt(btn.getAttribute('data-col'));
      sortTable(col);
    });
  });

  document.getElementById('refreshInstructores')?.addEventListener('click', ()=>{
    if(searchInput) searchInput.value='';
    if(filtroEspecialidad) filtroEspecialidad.value='';
    if(filtroCiudad) filtroCiudad.value='';
    if(filtroActivo) filtroActivo.value='';
    filtrar();
  });
})();
