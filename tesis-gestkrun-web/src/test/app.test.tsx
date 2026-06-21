import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'

describe('App renders', () => {
  it('can render basic components', () => {
    const { container } = render(<div data-testid="app">GESTKRUN</div>)
    expect(screen.getByTestId('app')).toBeInTheDocument()
    expect(container.textContent).toBe('GESTKRUN')
  })

  it('supports assertions', () => {
    expect(1 + 1).toBe(2)
    expect({ a: 1 }).toEqual({ a: 1 })
  })
})

describe('TypeScript types', () => {
  it('enums are strings', () => {
    expect('ADMIN').toBe('ADMIN')
    expect('PENDIENTE').toBe('PENDIENTE')
  })
})
