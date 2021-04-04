'use strict'

// code mostly from https://github.com/sindresorhus/ora

const screen = require('./screen')

class Spinner {
  constructor (options) {
    this.options = Object.assign({
      text: ''
    }, options)

    this.ansi = require('ansi-escapes')
    let spinners = require('./spinners.js')

    this.command = this.options.command
    this.color = this.options.color || 'heroku'
    this.spinner = process.platform === 'win32' ? spinners.line : (this.options.spinner ? spinners[this.options.spinner] : spinners.dots2)
    this.text = this.options.text
    this.interval = this.options.interval || this.spinner.interval || 100
    this.id = null
    this.frameIndex = 0
    this.stream = this.options.stream || process.stderr
  }

  start () {
    if (this.id) return
    this.enabled = true
    this.stream.write(this.ansi.cursorLeft)
    this.stream.write(this.ansi.eraseLine)
    this.stream.write(this.ansi.cursorHide)
    this._render()
    this.id = setInterval(this._spin.bind(this), this.interval)
    process.on('SIGWINCH', this._sigwinch = this._render.bind(this))
  }

  stop (status) {
    if (status && !this.enabled) console.error(` ${status}`)
    if (!this.enabled) return
    if (status) this._status = status

    process.removeListener('SIGWINCH', this._sigwinch)
    clearInterval(this.id)
    this.id = null
    this.enabled = false
    this.frameIndex = 0
    this._render()
    this.stream.write(this.ansi.cursorShow)
  }

  get status () {
    return this._status
  }

  set status (status) {
    this._status = status
    if (this.enabled) this._render()
    else this.command.stderr.write(` ${this.status}\n${this.text}`)
  }

  get text () {
    return this._text
  }

  set text (text) {
    this._text = text
    if (this.enabled) this._render()
  }

  clear () {
    if (!this._output) return
    this.stream.write(this.ansi.cursorUp(this._lines(this._output)))
    this.stream.write(this.ansi.eraseDown)
  }

  _render () {
    this.clear()
    this._output = `${this.text}${this.enabled ? ' ' + this._frame() : ''} ${this.status ? this.status : ''}\n`
    this.stream.write(this._output)
  }

  _lines (s) {
    return this.command.color.stripColor(s)
      .split('\n')
      .map(l => Math.ceil(l.length / this._width))
      .reduce((c, i) => c + i, 0)
  }

  get _width () {
    return screen.errtermwidth
  }

  _spin () {
    this.stream.write(this.ansi.cursorUp(this._lines(this._output)))
    let y = this._lines(this.text) - 1
    let lastline = this.command.color.stripColor(this.text).split('\n').pop()
    let x = 1 + lastline.length - (this._lines(lastline) - 1) * this._width
    this.stream.write(this.ansi.cursorMove(x, y))
    this.stream.write(this._frame())
    this.stream.write(this.ansi.cursorDown(this._lines(this._output) - y))
    this.stream.write(this.ansi.cursorLeft)
    this.stream.write(this.ansi.eraseLine)
  }

  _frame () {
    var frames = this.spinner.frames
    var frame = frames[this.frameIndex]
    if (this.color) frame = this.command.color[this.color](frame)
    this.frameIndex = ++this.frameIndex % frames.length
    return frame
  }
}

module.exports = Spinner
