import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  serverExternalPackages: ['@copilotkit/runtime'],
  reactCompiler: true,
}

export default nextConfig
