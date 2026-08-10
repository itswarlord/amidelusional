import { Inter, Sora } from 'next/font/google'
import './globals.css'
import { Navbar } from '@/components/navbar'
import { Footer } from '@/components/footer'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })
const sora = Sora({ subsets: ['latin'], variable: '--font-display' })

export const metadata = {
  title: 'Am I Delusional? — AI Relationship Diagnostic Tool',
  description:
    'Clinical relationship insights from your WhatsApp chat history. Powered by BAAI, LangChain, and Pinecone RAG — custom-trained for Indian relationships.',
  generator: 'v0.app',
}

export const viewport = {
  colorScheme: 'light',
  themeColor: '#3072dd',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${sora.variable} bg-background`}>
      <body className="antialiased font-sans flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-1">{children}</div>
        <Footer />
      </body>
    </html>
  )
}
