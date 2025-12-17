import { AlertDialogQuickOpen } from './_components/alert-dialog-quick-open'
import { Counter } from './_components/counter'
import { AppleHelloEnglishEffect } from './_components/hello'
import { ThemeToggle } from './_components/theme-toggle'

export default function HomePage() {
  return (
    <div className="text-center">
      <main className="min-h-screen flex flex-col items-center justify-center gap-5">
        <ThemeToggle />
        Hello World
        <Counter />
        <div className="flex flex-col gap-4">
          <AppleHelloEnglishEffect />
        </div>
        <AlertDialogQuickOpen />
      </main>
    </div>
  )
}
