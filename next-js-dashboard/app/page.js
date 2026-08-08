import Link from 'next/link'
import { ArrowRight, MessageCircle, Upload, FileText, Brain, HeartPulse, ShieldCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'

const steps = [
  {
    number: '1',
    icon: MessageCircle,
    title: 'Provide Background',
    description:
      'Type in background context about your relationship — ages, how you met, and key dynamics — directly in the tool prompt.',
  },
  {
    number: '2',
    icon: Upload,
    title: 'Upload Chat Export',
    description:
      'Export your WhatsApp conversation as a .txt file and upload it to our secure, encrypted analysis engine.',
  },
  {
    number: '3',
    icon: FileText,
    title: 'Get Your PDF Report',
    description:
      'Receive a comprehensive clinical-grade PDF report with relationship scores, behavioral patterns, and actionable insights.',
  },
]

const features = [
  {
    icon: Brain,
    title: 'Psychology Frameworks',
    description:
      "Applies attachment theory, John Gottman's research, and CBT principles to analyze communication patterns.",
  },
  {
    icon: HeartPulse,
    title: 'Indian Relationship Context',
    description:
      'Custom-trained on Indian relationship dynamics, cultural nuances, and communication styles.',
  },
  {
    icon: ShieldCheck,
    title: 'Clinical-Grade Accuracy',
    description:
      'Powered by Pinecone RAG and Gemini AI for deep semantic analysis beyond surface-level sentiment.',
  },
]

export default function HomePage() {
  return (
    <main>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0 -z-10"
          style={{
            background:
              'radial-gradient(ellipse 80% 60% at 50% -10%, oklch(0.75 0.1 285 / 0.18) 0%, transparent 70%)',
          }}
          aria-hidden="true"
        />

        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-20 pb-24 text-center">
          <div className="mb-2">
            <span className="inline-block rounded-full border border-border/80 bg-card px-4 py-1 text-xs font-medium uppercase tracking-widest text-muted-foreground shadow-sm">
              Team Warlords &nbsp;&middot;&nbsp; Hackathon Project
            </span>
          </div>

          <h1 className="mt-6 font-display text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-foreground text-balance leading-[1.08]">
            Am I&nbsp;
            <span
              style={{
                background: 'linear-gradient(135deg, oklch(0.38 0.14 265), oklch(0.65 0.14 186))',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              Delusional?
            </span>
          </h1>

          <p className="mt-3 text-sm font-medium text-muted-foreground tracking-wide">
            by Vansh Aggarwal
          </p>

          <p className="mt-6 mx-auto max-w-2xl text-lg sm:text-xl text-muted-foreground leading-relaxed text-pretty">
            Clinical relationship insights from your chat history. Our AI uses behavioral
            psychology frameworks to diagnose relationship health &mdash; custom-trained for{' '}
            <span className="text-foreground font-medium">Indian relationships</span> with real
            psychological scoring.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              asChild
              size="lg"
              className="gap-2 bg-primary hover:bg-primary/90 text-primary-foreground shadow-md px-8 text-base"
            >
              <Link href="/tool">
                Analyze My Relationship
                <ArrowRight size={18} />
              </Link>
            </Button>
            <Button
              asChild
              variant="outline"
              size="lg"
              className="px-8 text-base text-muted-foreground hover:text-foreground"
            >
              <Link href="/about">Learn More</Link>
            </Button>
          </div>

          <div className="mt-14 flex flex-wrap items-center justify-center gap-x-8 gap-y-3">
            {['Gemini AI', 'LangChain', 'Pinecone RAG', 'ReportLab PDF'].map((tech) => (
              <span key={tech} className="text-xs font-medium text-muted-foreground/70 tracking-wide">
                {tech}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Features row */}
      <section className="bg-card border-y border-border/60 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map(({ icon: Icon, title, description }) => (
              <div
                key={title}
                className="flex flex-col gap-3 p-6 rounded-xl bg-background border border-border/60"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary text-primary">
                  <Icon size={20} />
                </div>
                <h3 className="font-display font-semibold text-base text-foreground">{title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <p className="text-xs font-semibold uppercase tracking-widest text-accent mb-3">
              How It Works
            </p>
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-foreground text-balance">
              Three steps to clarity
            </h2>
            <p className="mt-3 text-muted-foreground text-base max-w-lg mx-auto">
              Get a clinical-grade relationship analysis in minutes, not months.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
            <div
              className="hidden md:block absolute top-10 left-[calc(16.67%-12px)] right-[calc(16.67%-12px)] h-px bg-border/60"
              aria-hidden="true"
            />
            {steps.map(({ number, icon: Icon, title, description }) => (
              <div
                key={number}
                className="flex flex-col items-center text-center gap-4 p-8 rounded-2xl bg-card border border-border/60 hover:border-accent/40 hover:shadow-sm transition-all"
              >
                <div className="relative flex h-14 w-14 items-center justify-center rounded-full bg-secondary border-2 border-background shadow">
                  <Icon size={22} className="text-primary" />
                  <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-accent text-accent-foreground text-[10px] font-bold">
                    {number}
                  </span>
                </div>
                <div>
                  <h3 className="font-display font-semibold text-base text-foreground mb-1.5">
                    {title}
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 text-center">
            <Button
              asChild
              size="lg"
              className="gap-2 bg-accent hover:bg-accent/90 text-accent-foreground shadow-md px-10"
            >
              <Link href="/tool">
                Try It Now
                <ArrowRight size={17} />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </main>
  )
}
