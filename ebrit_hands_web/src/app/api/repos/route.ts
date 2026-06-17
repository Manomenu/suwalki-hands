import { NextResponse } from 'next/server'

export async function GET() {
  const repos = []
  let i = 1
  while (process.env[`GITLAB_REPO_${i}`]) {
    const projectId = parseInt(process.env[`GITLAB_PROJECT_ID_${i}`] || '0', 10)
    repos.push({ id: projectId, name: process.env[`GITLAB_REPO_${i}`] as string })
    i++
  }
  return NextResponse.json(repos)
}
