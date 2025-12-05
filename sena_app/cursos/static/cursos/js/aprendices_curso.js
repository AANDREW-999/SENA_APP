(function(){
  const table = document.querySelector('.sena-table');
  const tbody = table ? table.querySelector('tbody') : null;
  const rows = tbody ? Array.from(tbody.querySelectorAll('tr')) : [];
  const fProg = document.getElementById('fProg');
  const fCurso = document.getElementById('fCurso');
  const totalBadge = document.querySelector('.badge.text-bg-success');

  if(!table || !tbody) return;

  function getCellText(tr, idx){
    const cell = tr.children[idx];
    return (cell ? cell.textContent : '').trim().toLowerCase();
  }

  function applyClientFilter(){
    const progTxt = (fProg?.value || '').trim().toLowerCase();
    const cursoTxt = (fCurso?.value || '').trim().toLowerCase();
    let visibles = 0;
    rows.forEach(tr => {
      const cursoCol = getCellText(tr, 0); // "codigo - nombre"
      const programaCol = getCellText(tr, 1); // "codigo - nombre"
      let show = true;
      if(progTxt){ show = programaCol.includes(progTxt); }
      if(show && cursoTxt){ show = cursoCol.includes(cursoTxt); }
      tr.style.display = show ? '' : 'none';
      if(show) visibles++;
    });
    if(totalBadge){
      const base = totalBadge.textContent.replace(/Total:\s*\d+/i,'').trim();
      totalBadge.textContent = `Total: ${visibles}`;
    }
  }

  [fProg, fCurso].forEach(el => {
    el && el.addEventListener('input', applyClientFilter);
    el && el.addEventListener('change', applyClientFilter);
  });

  // Ordenamiento por columna al hacer click en thead th
  const sortState = {};
  const ths = table.querySelectorAll('thead th');
  function sortByCol(colIdx){
    const dir = sortState[colIdx] === 'asc' ? 'desc' : 'asc';
    sortState[colIdx] = dir;
    const sorted = rows.slice().sort((a,b)=>{
      const aTxt = getCellText(a, colIdx);
      const bTxt = getCellText(b, colIdx);
      const aNum = Number(aTxt);
      const bNum = Number(bTxt);
      if(!Number.isNaN(aNum) && !Number.isNaN(bNum)){
        return dir === 'asc' ? (aNum - bNum) : (bNum - aNum);
      }
      if(aTxt < bTxt) return dir === 'asc' ? -1 : 1;
      if(aTxt > bTxt) return dir === 'asc' ? 1 : -1;
      return 0;
    });
    sorted.forEach(tr => tbody.appendChild(tr));
  }
  ths.forEach((th, idx)=>{
    th.addEventListener('click', function(){
      sortByCol(idx);
    });
  });
})();
