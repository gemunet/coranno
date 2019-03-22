axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

Vue.use(VueShortkey, {
  prevent: ['input', 'textarea'],
});


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],

  data() {
    return {
      startOffset: 0,
      endOffset: 0,
      chunks: [],
    };
  },

  mounted: function() {
    //document.addEventListener("mouseup", this.setSelectedRange);
    document.addEventListener("click", this.setSelectedRange);
  },

  methods: {
    isIn(label) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if (a.label === label.id) {
          return a;
        }
      }
      return false;
    },

    async addLabel(label) {
      const a = this.isIn(label);
      const isSubsChunk= this.isContainTaggedChunk(this.docs[this.pageNumber].start, this.docs[this.pageNumber].end);
      if (a && !isSubsChunk) {
        this.removeLabel(a);
      } else {
        const docId = this.docs[this.pageNumber].id;
        const payload = {
          label: label.id,
          start: this.docs[this.pageNumber].start,
          end: this.docs[this.pageNumber].end,
        };

        // si se ha seleccionado un parrafo
        let isSplit = false;
        if(this.validRange()) {
          payload.start = this.startOffset;
          payload.end = this.endOffset;
          isSplit = true;
        }

        // validamos que no se este sombrando una anotacion
        if(this.isContainTaggedChunk(payload.start, payload.end)) {
          console.warn('Seleccion invalida!');
          return;
        }

        await axios.post(`docs/${docId}/annotations/`, payload).then((response) => {
          this.annotations[this.pageNumber].push(response.data);
        });

        if(isSplit) {
          this.search();
        }
      }
    },
    
    isInTaggedChunk(start, end) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if(a.start <= start && a.end >= end) {
          return true;
        }
      }
      return false;
    },

    isContainTaggedChunk(start, end) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if((start < a.start && end >= a.end) ||
            (start <= a.start && end > a.end)) {
          return true;
        }
      }
      return false;
    },

    setSelectedRange(e) {
      console.debug(e);
      let offset = parseInt(e.target.getAttribute('data-offset'));

      if(isNaN(offset) || e.target.firstChild.nodeName != '#text' || !e.target.classList.contains('contentText')) {
        this.startOffset = 0;
        this.endOffset = 0;
        window.getSelection().collapseToEnd();
        return;
      }

      let start;
      let end;
      if (window.getSelection) {
        const range = window.getSelection().getRangeAt(0);
        start = range.startOffset + offset;
        end = range.endOffset + offset;
      }

      if(this.isInTaggedChunk(start, end)) {
        let node = e.target.firstChild;
        let range = document.createRange();
        range.setStart(node, 0);
        range.setEnd(node, node.length);

        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);

        start = offset;
        end = offset+node.length;
      }

      this.startOffset = start;
      this.endOffset = end;
      console.log(start, end);
    },

    validRange() {
      if (this.startOffset === this.endOffset) {
        return false;
      }
      if (this.startOffset > this.docs[this.pageNumber].text.length || this.endOffset > this.docs[this.pageNumber].text.length) {
        return false;
      }
      if (this.startOffset < 0 || this.endOffset < 0) {
        return false;
      }
      return true;
    },
    
    makeLabel() {
      const label = {
        id: 0,
        label: -1,
        start: -1,
        end: -1,
      };
      return label;
    },

    add_chunk(res, ann) {
      if(ann.start >= ann.end) return;
      if(!('k'+ann.start in res)) {
        res['k'+ann.start] = {'start': ann.start, 'end': ann.end, 'annotations': []};
      }
      res['k'+ann.start]['annotations'].push(ann.label);
    },

    update_chunks() {
      if(!this.docs[this.pageNumber]) return;
      let text = this.docs[this.pageNumber].text;
      let offset = this.docs[this.pageNumber].start;
      let sorted_annotations = this.annotations[this.pageNumber].concat().sort((a, b) => a.start - b.start);

      const res = [];
      let left = offset;
      for (let i = 0; i < sorted_annotations.length; i++) {
        const e = sorted_annotations[i];
        this.add_chunk(res, {'start': left, 'end': e.start, 'label': this.makeLabel()});
        this.add_chunk(res, {'start': e.start, 'end': e.end, 'label': e});
        left = e.end;
      }
      this.add_chunk(res, {'start': left, 'end': offset+text.length, 'label': this.makeLabel()});

      this.chunks = Object.keys(res).map(function(v) {return res[v]});
      console.debug('CHUNKS', this.chunks);
    }
  },

  watch: {
    pageNumber() {
      this.update_chunks();
    },
    annotations() {
      this.update_chunks();
    }
  },
});
