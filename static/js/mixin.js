axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');
const project_id = window.location.href.split('/').slice(4, 5).join('/');

const annotationMixin = {
  data() {
    return {
      pageNumber: 0,
      docs: [],
      annotations: [],
      labels: [],
      guideline: '',
      total: 0,
      remaining: 0,
      searchQuery: '',
      url: '',
      picked: 'all',
      count: 0,
      isActive: false,
    };
  },

  methods: {
    async nextPage() {
      this.pageNumber += 1;
      if (this.pageNumber === this.docs.length) {
        if (this.next) {
          this.url = this.next;
          await this.search();
          this.pageNumber = 0;
        } else {
          this.pageNumber = this.docs.length - 1;
        }
      }
    },

    async prevPage() {
      this.pageNumber -= 1;
      if (this.pageNumber === -1) {
        if (this.prev) {
          this.url = this.prev;
          await this.search();
          this.pageNumber = this.docs.length - 1;
        } else {
          this.pageNumber = 0;
        }
      }
    },

    async search() {
      await axios.get(this.url).then((response) => {
        this.docs = []
        for(let i=0; i<response.data.results.length; i++) {
          doc = response.data.results[i];
          for(s=0; s<doc.sentences.length; s++) {
            sentence = doc.sentences[s];
            
            annotations = [];
            for(a=0; a<doc.annotations.length; a++) {
              ann = doc.annotations[a];
              if(ann.start >= sentence.start && ann.end <= sentence.end) {
                annotations.push(ann);
              }
            }

            this.docs.push({
              'id': doc.id,
              'file': doc.file,
              'text': sentence.text,
              'start': sentence.start,
              'end': sentence.end,
              'annotations': annotations,
            })
          }
        }
        
        this.next = response.data.next;
        this.prev = response.data.previous;
        this.count = response.data.count;
        this.annotations = [];
        for (let i = 0; i < this.docs.length; i++) {
          const doc = this.docs[i];
          this.annotations.push(doc.annotations);
        }
      });
    },

    getState() {
      if (this.picked === 'all') {
        return '';
      }
      if (this.picked === 'active') {
        return 'true';
      }
      return 'false';
    },

    async submit() {
      const state = this.getState();
      this.url = `docs/?q=${this.searchQuery}&is_checked=${state}`;
      await this.search();
      this.pageNumber = 0;
    },

    removeLabel(annotation) {
      const docId = this.docs[this.pageNumber].id;
      axios.delete(`docs/${docId}/annotations/${annotation.id}`).then((response) => {
        const index = this.annotations[this.pageNumber].indexOf(annotation);
        this.annotations[this.pageNumber].splice(index, 1);
      });
    },
  },

  watch: {
    picked() {
      this.submit();
    },

    annotations() {
      // fetch progress info.
      axios.get(`/api/projects/${project_id}/`).then((response) => {
        this.total = response.data.progress.total;
        this.remaining = this.total-response.data.progress.current;
      });
    },
  },

  created() {
    axios.get(`/api/projects/${project_id}/`).then((response) => {
      this.labels = response.data.labels;
    });
    axios.get().then((response) => {
      this.guideline = response.data.guideline;
    });
    this.submit();
  },

  computed: {
    achievement() {
      const done = this.total - this.remaining;
      const percentage = Math.round(done / this.total * 100);
      return this.total > 0 ? percentage : 0;
    },

    compiledMarkdown() {
      return marked(this.guideline, {
        sanitize: true,
      });
    },

    id2label() {
      let id2label = {};
      for (let i = 0; i < this.labels.length; i++) {
        const label = this.labels[i];
        id2label[label.id] = label;
      }
      return id2label;
    },

    progressColor() {
      if (this.achievement < 30) {
        return 'is-danger';
      }
      if (this.achievement < 70) {
        return 'is-warning';
      }
      return 'is-primary';
    },
  },
};
