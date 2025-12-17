import { Spinner } from '@/shared/components/ui/spinner'

export default function Loading() {
  return (
    <div className="w-dvw h-dvh flex items-center justify-center">
      <Spinner className="size-12" />
    </div>
  )
}
