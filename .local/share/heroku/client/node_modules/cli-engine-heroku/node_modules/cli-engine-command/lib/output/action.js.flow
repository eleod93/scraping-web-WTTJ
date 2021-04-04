// @flow

import type Spinner from './spinner'
import type Output from '.'

type Task = {
  spinner?: Spinner,
  status: ?string,
  message: string,
  paused?: boolean
}

export default class Action {
  out: Output
  task: ?Task = null

  constructor (out: Output) {
    this.out = out
  }

  start (message: string, status: ?string) {
    const msg = `${message}...`
    if (this.task) {
      this.task.message = message
      if (this.task.spinner) {
        this.task.spinner.text = msg
        this.task.spinner.status = status
      } else this.out.stderr.write(`\n${msg}` + (status ? ` ${status}` : ''))
    } else {
      this.task = ({message, status}: Task)
      if (this.displaySpinner) {
        const Spinner = require('./spinner')
        this.task.spinner = new Spinner({text: msg, command: this.out, status})
        this.task.spinner.start()
      } else this.out.stderr.write(`${msg}` + (status ? ` ${status}` : ''))
    }
  }

  get displaySpinner (): boolean {
    return !this.out.mock && !this.out.config.debug && !!process.stdin.isTTY && !!process.stderr.isTTY && !process.env.CI && process.env.TERM !== 'dumb'
  }

  stop (msg: string = 'done') {
    if (!this.task) return
    this.start(this.task.message, msg)
    if (this.task && this.task.spinner) this.task.spinner.stop(msg)
    else this.out.stderr.write('\n')
    delete this.task
  }

  pause (fn: Function) {
    let spinner = this.task ? this.task.spinner : null
    if (this.task) {
      if (this.task.paused) return fn()
      this.task.paused = true
      if (spinner) {
        spinner.stop()
        spinner.clear()
      } else {
        delete this.task
        this.out.stderr.write('\n')
      }
    }
    fn()
    if (this.task) this.task.paused = false
    if (spinner) {
      this.out.stderr.write('\n')
      spinner.start()
    }
  }
}
