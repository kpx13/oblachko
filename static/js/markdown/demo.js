var opts = {
  basePath: '',
  theme: {
    base: '/static/js/markdown/epiceditor.css',
    preview: '/static/js/markdown/bartik.css',
    editor: '/static/js/markdown/epic-light.css'
  }
}

var editor = new EpicEditor(opts).load();