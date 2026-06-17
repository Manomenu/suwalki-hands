const BASE_URL = process.env.YTRACK_CHANNEL_URL ?? 'http://localhost:6010'

export const ytracksChannelClient = {
  async submitTask(body: object): Promise<{ data: unknown; status: number }> {
    const res = await fetch(`${BASE_URL}/webhook/mock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    return { data: await res.json(), status: res.status }
  },
}
