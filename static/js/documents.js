axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

const vm = new Vue({
    el: '#documents_root',
    delimiters: ['[[', ']]'],

    methods: {
        deleteDocument(id) {
          axios.delete(`${baseUrl}/api/documents/${id}/`).then((response) => {
            location.reload();
          });
        },
    }
});