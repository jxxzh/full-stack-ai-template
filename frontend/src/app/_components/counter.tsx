'use client'

import { atom, useAtom } from 'jotai'
import { Button } from '@/shared/components/ui/button'

const countAtom = atom(0)
countAtom.debugLabel = 'countAtom'

export const Counter = () => {
  const [count, setCount] = useAtom(countAtom)
  const inc = () => setCount((c) => c + 1)
  return (
    <div>
      <h2>Counter</h2>
      {count} <Button onClick={inc}>+1</Button>
      <br />
      <br />
    </div>
  )
}
