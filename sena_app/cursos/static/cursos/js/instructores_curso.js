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
    if(totalBadge){ totalBadge.textContent = `Total: ${visibles}`; }
  }

  [fProg, fCurso].forEach(el => {
    el && el.addEventListener('input', applyClientFilter);
    el && el.addEventListener('change', applyClientFilter);
  });

  const sortState = {};
  const ths = table.querySelectorAll('thead th');
  function sortByCol(colIdx){
    const dir = sortState[colIdx] === 'asc' ? 'desc' : 'asc';
    sortState[colIdx] = dir;
    const visibleRows = rows.filter(r => r.style.display !== 'none');
    visibleRows.sort((a,b)=>{
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
    visibleRows.forEach(tr => tbody.appendChild(tr));
  }
  ths.forEach((th, idx)=>{
    const isActions = idx === ths.length - 1;
    if(isActions) return;
    th.style.cursor = 'pointer';
    th.title = 'Ordenar';
    th.addEventListener('click', ()=> sortByCol(idx));
  });

  // Reset opcional
  const resetBtn = document.getElementById('refreshInstructoresCurso');
  resetBtn && resetBtn.addEventListener('click', () => {
    if(fProg) fProg.value='';
    if(fCurso) fCurso.value='';
    applyClientFilter();
  });

  applyClientFilter();
})();
