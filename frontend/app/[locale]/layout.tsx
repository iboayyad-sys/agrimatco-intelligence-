import type { Metadata } from 'next'
import { ReactNode } from 'react'
import { getMessages } from 'next-intl/server'
import { NextIntlClientProvider } from 'next-intl'
import { Providers } from './providers'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Agrimatco Smart Crop Advisor',
  description: 'AI-powered agricultural assistant for crop health diagnosis',
  icons: {
    icon: '/favicon.ico',
  },
}

export default async function RootLayout({
  children,
  params: { locale },
}: {
  children: ReactNode
  params: { locale: string }
}) {
  const messages = await getMessages()

  return (
    <html lang={locale} suppressHydrationWarning>
      <body>
        <NextIntlClientProvider messages={messages}>
          <Providers>{children}</Providers>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
