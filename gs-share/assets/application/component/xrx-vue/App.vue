<template>
<div class="xrx-vue">
  <div v-if="showToolbar" class="panel-heading">
    <div class="form-inline xrx-toolbar">
      <div v-if="showToolbarModes" class="input-group">
        <button title="Hover" @click="setMode('HoverMult')" v-bind:class="`btn btn-default ${!!mode.match(/^Hover/)?'active':''}`"><img style="height:20px;" src="https://awe.do/images/canvas/hand.svg"/></button>
        <button @click="setMode('Modify')" title="Modify" v-bind:class="`btn btn-default ${mode === 'Modify'?'active':''}`"><img style="height:20px;" src="https://awe.do/images/canvas/hand-point.svg"/></button>
        <button @click="setMode('Select')" title="Select" v-bind:class="`btn btn-default ${mode === 'Select'?'active':''}`"><img style="height:20px;" src="https://awe.do/images/canvas/cursor.svg"/></button>
        <select @click="setMode($event.target.value)" v-if="showToolbarModesList" style="width: inherit" class="form-control">
          <option v-for="value in modesEnabled" v-bind:value="value" v-bind:disabled="modesAvailable.find(x =&gt; x.value == value).disabled" v-bind:selected="value == mode">{{ modesAvailable.find(x => x.value == value).text }}</option>
        </select>
      </div>
      <div v-if="selectedShape" class="input-group btn-group">
        <!-- <button title="Copy" @click="copySelected" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/copy.svg"/></button> -->
        <button title="Remove" @click="removeSelected" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/remove.svg"/></button>
      </div>
      <div v-if="showToolbarShapes" class="input-group btn-group">
        <button title="Polygon" @click="drawShape('Polygon')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/polygon.svg"/></button>
        <button title="Rectangle" @click="drawShape('Rect')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/rectangle.svg"/></button>
        <button title="Ellipse" @click="drawShape('Ellipse')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/ellipsis.svg"/></button>
        <button title="Circle" @click="drawShape('Circle')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/circle.svg"/></button>
        <button title="Polyline" @click="drawShape('Polyline')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/polyline.svg"/></button>
        <button title="line" @click="drawShape('Line')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/line.svg"/></button>

        <button title="Arrow" @click="loadSvg('arrow')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/arrow.png"/></button>


      </div>
      <div v-if="showToolbarFile" class="input-group">
        <button title="Save SVG" @click="showExport" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/save.svg"/></button>
        <button title="Load SVG" @click="showImport" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/upload.svg"/></button>
        <button title="Background Image" @click="showImageModal" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/image.svg"/></button>
      </div>
      <div v-if="showToolbarZoom" class="input-group btn-group">
        <button title="Zoom in" @click="zoom('in')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/zoom-in.svg"/></button>
        <button title="Zoom out" @click="zoom('out')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/zoom-out.svg"/></button><span class="dropdown">
          <button type="button" data-toggle="dropdown" class="btn btn-default dropdown-toggle">{{ parseInt(zoomValue * 100) }} %<span class="caret"></span></button>
          <ul class="dropdown-menu">
            <li><a href="#" @click="zoom(1)">100 %</a></li>
            <li><a href="#" @click="zoom('fit')">Fit to canvas</a></li>
            <li><a href="#" @click="zoom('width')">Fit to width</a></li>
            <li><a href="#" @click="zoom('height')">Fit to height</a></li>
          </ul></span>
      </div>
      <div v-if="showToolbarRotate" class="input-group btn-group">
        <button title="Rotate right" @click="rotate('Left')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/rotate-right.svg"/></button>
        <button title="Rotate left" @click="rotate('Right')" class="btn btn-default"><img style="height:20px;" src="https://awe.do/images/canvas/rotate-left.svg"/></button>
      </div>
    </div>
  </div>
  <!-- Canvas-->
  <div style="position: relative">
    <div ref="image" v-bind:style="`width: ${width}; height: ${height}`"></div>
    <div v-if="enableThumb" ref="thumb" v-bind:class="{thumb, 'fade-out':!thumbVisible}" v-bind:style="thumbStyle"></div>
  </div>
  <!-- SVG Import Modal-->
  <div role="dialog" ref="importModal" tabindex="-1" class="import-modal modal fade">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">Import from SVG</div>
        <div class="modal-body">
          <textarea v-model="svgImport" placeholder="SVG here" class="form-control"></textarea>
          <template>
            <button @click="loadSvg(this.svgImport)" class="form-control btn btn-success">Load</button>
          </template>
        </div>
      </div>
    </div>
  </div>
  <!-- SVG Export Modal-->
  <div role="dialog" ref="exportModal" tabindex="-1" class="export-modal modal fade">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">Export as SVG</div>
        <div class="modal-body">
          <textarea v-model="svgExport" placeholder="SVG here" readonly="readonly" class="form-control"></textarea>
        </div>
      </div>
    </div>
  </div>
  <!-- Background image modal-->
  <div role="dialog" ref="imageModal" tabindex="-1" class="image-modal modal fade">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">Set background image</div>
        <div class="modal-body">
          <input format="url" v-model="imageBackground" placeholder="Image URL" class="form-control"/>
          <button @click="loadImage(this.imageBackground)" class="form-control btn btn-success">Set background image</button>
        </div>
      </div>
    </div>
  </div>

</div>
</template>

<script>
import axios from 'axios';
import XrxUtils from 'semtonotes-utils'
var thumbHideTimeoutId = null

export default {

  name: 'xrx-vue',

  data() { return {
    mode: this.initialMode,
    svgExport: '',
    svgImport: '',
    zoomValue: this.initialZoom,
    image: null,
    thumbVisible: false,
    selectedShape: null,
    imageBackground: null,
  }},

  /**
   * ### Properties
   *
   */
  props: {


    /**
     * 
     * #### `width`
     * Width of the canvas (**not** the image). Default: `600`
     * 
     * #### `height`
     * Height of the canvas (**not** the image). Default: `400`
     */
    width:  {type: Number, default: innerWidth},
    height: {type: Number, default: innerHeight-200},

    /**
     * 
     * #### `enable-thumb`
     * Whether the thumb navigation is enabled. Defaut: `true`
     * 
     * #### `thumb-width`
     * Width of the nav thumb (**not** the thumbnail image). Default: `120`
     * 
     * #### `thumb-background`
     * Fixed thumbnail image. Default: `''` (none, use current canvas image)
     * 
     * #### `thumb-height`
     * Height of the nav thumb (**not** the thumbnail image). Default: `120`
     * 
     * #### `thumb-timeout`
     * Time in ms after which to hide the thumb. Default: `1000`
     */

    enableThumb:     {type: Boolean, default: true},
    thumbBackground: {type: String, default: ''},
    thumbWidth:      {type: Number, default: 120},
    thumbHeight:     {type: Number, default: 120},
    thumbTimeout:    {type: Number, default: 1000},

    /**
     * 
     * #### `show-toolbar`
     * Whether to show or hide the complete toolbar. Default: `true`
     * 
     * #### `show-toolbar-modes`
     * Whether to show the modes toolbar. Default: `true`
     * 
     * #### `show-toolbar-mode-list`
     * Whether to show the list of modes. Default: `false`
     * 
     * #### `show-toolbar-shapes`
     * Whether to show the shapes toolbar. Default: `true`
     * 
     * #### `show-toolbar-file`
     * Whether to show the file toolbar. Default: `true`
     * 
     * #### `show-toolbar-zoom`
     * Whether to show the zoom toolbar. Default: `true`
     * 
     * #### `show-toolbar-rotate`
     * Whether to show the rotate toolbar. Default: `true`
     */
    showToolbar:          {type: Boolean, default: true},
    showToolbarModes:     {type: Boolean, default: true},
    showToolbarModesList: {type: Boolean, default: false},
    showToolbarShapes:    {type: Boolean, default: true},
    showToolbarFile:      {type: Boolean, default: false},
    showToolbarZoom:      {type: Boolean, default: true},
    showToolbarRotate:    {type: Boolean, default: true},

    /**
     * 
     * #### `zoom-factor-max`
     * Maximum zoom factor. Default: `4`
     * 
     * #### `initial-zoom`
     * Initial zoom. Default: `1` (== 100%)
     */
    zoomFactorMax: {type: Number, default: 4},
    initialZoom: {type: Number, default: 1},

    /**
     * 
     * #### `initial-svg`
     * Initial SVG value
     * 
     * #### `grouped`
     * Whether shapes loaded from SVG should be grouped. Default: `false`
     */
    initialSvg: {type: String},
    grouped: {type: Boolean, default: true},

    /**
     * 
     * #### `initial-image`
     * Initial background image to load.
     */
    initialImage: {type: String, default: require('@share/component/xrx-vue/assets/1024px-Ghostscript_Tiger.svg.png'), required: true},

    // initialImage: {type: String, default: require('https://awe.do/images/canvas/1024px-Ghostscript_Tiger.svg.png'), required: true},

    /**
     * 
     * #### `initia-mode`
     * Initial mode. Default `HoverMult`
     */
    initialMode: {type: String, default: 'HoverMult'},

    modesEnabled: {type: Array, default(){return[
      'Disabled',
      'Hover',
      'HoverMult',
      'Modify',
      'Create',
      'Select'
    ]}},
    modesAvailable: {type: Array, default(){return [
      {value: 'Hover', text: 'Hover'},
      {value: 'HoverMult', text: 'Hover (multiple)'},
      {value: 'Modify', text: 'Modify'},
      {value: 'Create', text: 'Create', disabled: true},
      {value: 'Select', text: 'Select'},
    ]}},

    /**
     * 
     * #### `xrx-style`
     * Styles to use for shapes in image. Default: `[see source]`
     * 
     * #### `thumb-xrx-style`
     * Styles to use for thumb shapes. Default: `{}`
     */
    thumbXrxStyle: {type: Object, default: () => {}},
    xrxStyle: {type: Object, default() { return {
      strokeColor: '#3B3BFF',
      fillColor: '#3B3BFF',
      strokeWidth: 2,
      fillOpacity: 0.4,
      hoverable: {
        strokeColor: '#00ff00',
        fillColor: '#00ff00',
        strokeWidth: 3,
        fillOpacity: 0.4,
      },
      creatable: {
        strokeColor: '#ff0000',
        fillColor: '#ff0000',
        strokeWidth: 3,
        fillOpacity: 0.4,
      },
      modifiable: {
        strokeColor: '#ff008f',
        fillColor: '#ff008f',
        strokeWidth: 3,
        fillOpacity: 0.4,
      },
      selectable: {
        strokeColor: '#ff00ff',
        fillColor: '#ff00ff',
        strokeWidth: 3,
        fillOpacity: 0.4,
      },
    }}},


  },

  /**
   * 
   * ### Events
   * 
   * #### `viewbox-changed`
   * The viewbox (visible layer) has changed.
   * 
   * #### `shape-created(shape)`
   * A new shape `shape` was created.
   * 
   * #### `shape-modified(shape)`
   * An existing shape `shape` was changed.
   * 
   * #### `shape-deleted(shape)`
   * A shape `shape` has been deleted by the user.
   * 
   * #### `shape-selected(shape)`
   * A shape `shape` has been selected by the user.
   * 
   * #### `shape-activated(shape)`
   * Shape `shape` is modifiable and has been activated
   * 
   * #### `shape-hover-in(shape)`
   * `mouseenter` on the `shape`.
   * 
   * #### `shape-hover-out(shape)`
   * `mouseleave` on the `shape`.
   * 
   * #### `mode-changed(from, to)`
   * The mode changed, it was `from`, now it is `to`.
   * 
   * #### `svg-changed(svg)`
   * The SVG changed to `svg`
   * 
   * #### `zoom-changed(now, before)`
   * Zoom value changed from `before` to `now`
   * 
   */
  mounted() {

    // ['load-image'].forEach((ev, ...args) => {
    //   console.info('EVENT', ev, args)
    // })

    if (this.enableThumb) {
      this._initThumb()
    }

    this._initCanvas()

    this.imageBackground = this.initialImage

    if (this.imageBackground) {
      this.image.setBackgroundImage(this.imageBackground, () => {
        if (this.initialSvg) {
          this.reset()
          this.loadSvg(this.initialSvg)
        }
        this.image.getViewbox().fit(true)
        this.image.draw()
        if (this.enableThumb) {
          const thumbBackground = this.thumbBackground || this.imageBackground
          this.thumb.setBackgroundImage(thumbBackground, () => {
            this.thumb.getViewbox().fit()
            this.thumb.draw()
          })
        }
      })
    }

  },

  computed: {
    imageDiv() { return this.$refs.image },
    thumbDiv() { return this.$refs.thumb },
    thumbStyle() {
      return [
        `width: ${this.thumbWidth}px`,
        `height: ${this.thumbHeight}px`,
        ].join(';')
    }
  },

  /**
   * 
   * ### Methods
   */
  methods: {

    async printThis() {
      console.log("printing..");
      const el = this.$refs.image;

      const options = {
        type: "dataURL"
      };
      const printCanvas = await html2canvas(el, options);
      
      const toImg = printCanvas.toDataURL("image/jpeg");

      // const link = document.createElement("a");
      // link.setAttribute("download", "download.png");
      // link.setAttribute(
      //   "href",
      //   printCanvas
      //     .toDataURL("image/png")
      //     .replace("image/png", "image/octet-stream")
      // );
      // link.click();


              axios.post('/send_replace_image', {
                toImg,
                id: this.initialImage.split('image_damage?id=')[1]
              });
            console.log("done");
    },



    _initThumb() {
      this.thumb = XrxUtils.createDrawing(this.thumbDiv, this.thumbWidth, this.thumbHeight)

      this.$on('rotate', (amount) => this.thumb.getViewbox()[`rotate${amount}`]())
      this.$on('load-image', (img, thumbBackground) => {
        thumbBackground = thumbBackground || this.thumbBackground || this.imageBackground
        this.thumb.setBackgroundImage(thumbBackground, () => {
          this.thumb.getViewbox().fit()
          this.thumb.draw()
        })
      })
      this.$on('viewbox-changed', () => {
        XrxUtils.navigationThumb(this.thumb, this.image, this.thumbXrxStyle)
        this.showThumb()
      })

      this.thumbDiv.addEventListener('mouseenter', () => this.thumbDiv.classList.add('invisible'))
      let thumbShowTimeoutId = null
      // TODO
      this.thumbImage = this.imageBackground
      this.thumbDiv.addEventListener('mouseleave', () => {
        clearTimeout(thumbShowTimeoutId)
        thumbShowTimeoutId = setTimeout(() => {
          this.thumbDiv.classList.remove('invisible')
        }, 1000)
      })
    },

    _initCanvas() {
      this.image = XrxUtils.createDrawing(this.imageDiv, this.width, this.height)
      this.$on('rotate', (amount) => this.image.getViewbox()[`rotate${amount}`]())
      this.$on('load-image', (img) => {
        img = img || this.imageBackground
        this.image.setBackgroundImage(img, () => {
          this.image.getViewbox().fit(true)
          this.image.draw()
          const {svgImport} = this
          if (svgImport) {
            this.reset()
            this.loadSvg(svgImport)
          }
        })
      })

      this.image.eventViewboxChange   = () => this.$emit('viewbox-changed')
      this.image.eventShapeCreated    = (shape) => this.$emit('shape-created', shape)
      this.image.eventShapeModify     = (shape) => this.$emit('shape-modified', shape)
      this.image.eventShapeActivated  = (shape) => this.$emit('shape-activated', shape)
      this.image.eventShapeSelected   = (shape) => this.$emit('shape-selected', shape)
      this.image.eventShapeUnselected = (shape) => this.$emit('shape-unselected', shape)
      this.image.eventShapeHoverIn    = (shape) => this.$emit('shape-hover-in', shape)
      this.image.eventShapeHoverOut   = (shape) => this.$emit('shape-hover-out', shape)

      this.$watch(() => this.svgExport, (svg) => {
      this.$emit('contentId', this.svgExport)
      this.$emit('svg-changed', svg)
      })
      this.$watch(() => this.zoomValue, (...args) => this.$emit('zoom-changed', ...args))

      this.$on('svg-loaded', () => this.exportSvg())

      this.$on('shape-activated', (shape) => {
        this.selectedShape = shape
      })
      this.$on('shape-selected', (shape) => {
        this.$emit('shape-unselected', this.selectedShape)
        this.selectedShape = this.image.getSelectedShape()
      })
      this.$on('shape-unselected', (shape) => {
        if (shape) {
          shape.getModifiable().selectOff()
        }
        this.selectedShape = null;
      })
      this.$on('shape-modified', (shape) => {
        this.exportSvg()
      })
      this.$on('shape-deleted', (shape) => {
        this.exportSvg()
      })
      this.$on('shape-created', (shape) => {
        this.applyStyles()
        this.setMode('Modify')
        this.image.getLayerShapeModify().activate(shape.getModifiable())
        shape.getModifiable().selectOn()
        this.exportSvg()
        document.activeElement.blur()
      })
      this.$on('mode-changed', (from, to) => {
        if (to === 'Hover' || to === 'HoverMult') {
          this.$emit('shape-unselected', this.selectedShape)
        }
      })
      this.$on('viewbox-changed', () => {
        this.zoomValue = this.image.getViewbox().getZoomValue()
        if (this.mode !== 'Modify')
          this.selectedShape = this.image.getSelectedShape()
      })

      this.image.getViewbox().setZoomFactorMax(this.zoomFactorMax)
      this.svgImport = this.initialSvg
      this.setMode(this.mode)
    },


    /**
     * 
     * #### `loadImage(img)`
     * - `@param String img` URL of the image. Defaults to `this.imageBackground`
     *   which defaults to [`initialImage`](#initialimage)
     */
    loadImage(img, thumb) {
      if (img) this.imageBackground = img
      this.$emit('load-image', img, thumb)
    },

    /**
     * 
     * #### `setMode(mode, ...args)`
     *
     * Sets the mode, passing further args to `setXXXMode`
     */
    setMode(mode, ...args) {
      if (mode === 'HoverMult') this.image.setModeHover(true);
      else this.image[`setMode${mode}`](...args);
      this.$emit('mode-changed', this.mode, mode)
      this.mode = mode
    },

    /**
     * 
     * #### `zoom(amount)`
     * 
     * Change the zoom level of the viewbox.
     * 
     * `amount` can be
     * - `in` to zoom in
     * - `out` to zoom out
     * - `fit` to make the image fit the canvas
     * - `width` to make the image width fit the canvas
     * - `height` to make the image height fit the canvas
     * - a number between `0` and [`zoomFactorMax`](#zoomfactormax) to zoom to that value
     */
    zoom(amount) {
      if (amount === 'in') this.image.getViewbox().zoomIn()
      else if (amount === 'out') this.image.getViewbox().zoomOut()
      else if (amount === 'fit') this.image.getViewbox().fit(true)
      else if (amount === 'width') this.image.getViewbox().fitToWidth(true)
      else if (amount === 'height') this.image.getViewbox().fitToHeight(true)
      else this.image.getViewbox().zoomTo(amount)
      this.zoomValue = this.image.getViewbox().getZoomValue()
      this.image.draw()
    },

    /**
     * 
     * #### `rotate(amount)`
     * 
     * Rotate the canvas `Left` or `Right`.
     */
    rotate(...args) {
      this.$emit('rotate', ...args)
    },

    /**
     * 
     * #### `applyStyles()`
     * 
     * Apply the defined style to all the shapes
     */
    applyStyles() {
      this.image.getLayerShape().getShapes().forEach(shape => {
        XrxUtils.applyStyle(shape, this.xrxStyle)
      })
    },

    /**
     * 
     * #### `drawShape(shapeName)`
     * 
     * `shapeName` can be one of:
     * - `Polygon`
     * - `Polyline`
     * - `Line`
     * - `Rect`
     * - `Circle`
     * - `Ellipse`
     */
    drawShape(shapeName) {
      const shape = new xrx.shape[shapeName](this.image)
      XrxUtils.applyStyle(shape, this.xrxStyle)
      this.setMode('Create', shape.getCreatable())
    },

    /**
     * 
     * #### `removeSelected`
     * 
     * Remove the currently selected shape
     */
    removeSelected() {
      if (window.confirm("Delete selected shape?")) {
        const shape = this.selectedShape
        this.image.removeShape(shape)
        this.setMode(this.initialMode)
        this.$emit('shape-unselected')
        this.$emit('shape-deleted', shape)
      }
      document.activeElement.blur()
    },

    /**
     * 
     * #### `copySelected()`
     * 
     * Copy the currently selected shape
     */
    copySelected() {
      const svg = XrxUtils.svgFromShapes(this.image.getSelectedShape())
      XrxUtils.drawFromSvg(svg, this.image)
      this.applyStyles()
    },

    /**
     * 
     * #### `showImport()`
     * 
     * Show the import modal
     */
    showImport() {
      this.svgImport = ''
      $(this.$refs.importModal).modal('show')
    },

    /**
     * 
     * #### `showExport()`
     * 
     * Show the export modal
     */
    showExport() {
      $(this.$refs.exportModal).one('shown.bs.modal', () => {
        this.$refs.exportModal.querySelector('textarea').select()
      })
      $(this.$refs.exportModal).modal('show')
    },

    /**
     * 
     * #### `reset()`
     * 
     * Reset the canvas and svg
     * 
     */
    reset() {
      if(!this.image.getLayerBackground().getImage().getWidth()) {
        console.error("Image not yet loaded? Width is zero...")
        return
      }
      this.image.getLayerShapeModify().removeShapes();
      this.image.getLayerShape().removeShapes();
      this.svgImport = ''
      this.$emit('reset')
    },

    /**
     * 
     * #### `loadSvg(svg)`
     * 
     * Load the SVG
     */
    loadSvg(svg) {
      if (! svg || svg === '<svg></svg>') {
        console.error("Refusing to draw empty SVG. Use 'reset()' to reset.")
        return
      }
      if (svg == 'arrow'){
      this.svgImport = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1024"><polyline points="89.19065657571832,436.0427031225639 89.19065657571832,436.0427031225639 212.78854017360186,334.4554015352624 193.62818099366413,369.63682146679116 212.8874402529234,334.0812659112356 176.5911439566271,345.93311776308747" /></svg>'
      // console.log("loadSvg", {grouped: this.grouped, svgImport: this.svgImport})
      XrxUtils.drawFromSvg(this.svgImport, this.image, {grouped: this.grouped})
      this.applyStyles()
      // $(this.$refs.importModal).modal('hide')
      // // console.log('svg-loaded')
      // this.$emit('svg-loaded')
      }
  
    },

    /**
     * 
     * #### `exportSvg()`
     * 
     * Export the SVG
     */
    exportSvg() {
      this.svgExport = XrxUtils.svgFromDrawing(this.image, {
        skipHeight: true
      })
    },

    /**
     * 
     * #### `showImageModal()`
     * 
     * Show the modal that allows changing the image url
     */
    showImageModal() {
      $(this.$refs.imageModal).modal('show')
    },

    /**
     * 
     * #### `showThumb()`
     * 
     * Show the navigation thumbnail and hide it again after
     * [`thumbTimeout`](#thumbtimeout)
     */
    showThumb() {
      this.thumbVisible = true;
      clearTimeout(thumbHideTimeoutId)
      thumbHideTimeoutId = setTimeout(() => this.thumbVisible = false, this.thumbTimeout)
    },

  }
}
</script>

<!-- vim: set sw=2 ts=2 :-->
