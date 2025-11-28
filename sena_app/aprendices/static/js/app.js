// Operaciones básicas de CRUD para Aprendices usando Fetch
// Asume que existen endpoints en las URLs de Django:
// - GET    /aprendices/ (lista)
// - POST   /aprendices/nuevo/ (crear)
// - GET    /aprendices/<id>/ (detalle)
// - POST   /aprendices/<id>/editar/ (actualizar)
// - POST   /aprendices/<id>/eliminar/ (eliminar)

(function () {
  const api = {
    listar: async (q = '') => {
      const url = q ? `/aprendices/?q=${encodeURIComponent(q)}` : '/aprendices/';
      const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      if (!res.ok) throw new Error('Error al listar aprendices');
      return await res.json().catch(() => null);
    },
    crear: async (data) => {
      const res = await fetch('/aprendices/nuevo/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Error al crear aprendiz');
      return await res.json().catch(() => null);
    },
    detalle: async (id) => {
      const res = await fetch(`/aprendices/${id}/`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      if (!res.ok) throw new Error('Error al obtener detalle');
      return await res.json().catch(() => null);
    },
    actualizar: async (id, data) => {
      const res = await fetch(`/aprendices/${id}/editar/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Error al actualizar aprendiz');
      return await res.json().catch(() => null);
    },
    eliminar: async (id) => {
      const res = await fetch(`/aprendices/${id}/eliminar/`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      if (!res.ok) throw new Error('Error al eliminar aprendiz');
      return await res.json().catch(() => null);
    }
  };

  // Exponer en window para uso desde templates
  window.AprendicesAPI = api;

  // Comportamiento de búsqueda rápida si existe el form en el header
  document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.querySelector('form.sena-search');
    if (searchForm) {
      searchForm.addEventListener('submit', (e) => {
        // Permitir funcionamiento estándar, pero podríamos interceptar si deseamos AJAX
        // e.preventDefault();
      });
    }
  });
})();

