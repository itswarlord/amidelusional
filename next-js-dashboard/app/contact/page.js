'use client'

import { useState } from 'react'
import { ExternalLink, Mail, Send, CheckCircle, MapPin, MessageSquare } from 'lucide-react'
import { Button } from '@/components/ui/button'

const contactDetails = [
  {
    icon: Mail,
    label: 'Email',
    value: 'vansh@iitg.ac.in',
    href: 'mailto:vansh@iitg.ac.in',
  },
  {
    icon: ExternalLink,
    label: 'GitHub',
    value: 'github.com/itswarlord/amidelusional',
    href: 'https://github.com',
  },
  {
    icon: MapPin,
    label: 'Based in',
    value: 'India',
    href: null,
  },
  {
    icon: MessageSquare,
    label: 'Response time',
    value: 'Within 24 hours',
    href: null,
  },
]

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', message: '' })
  const [submitted, setSubmitted] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setSubmitted(true)
  }

  return (
    <main className="py-16">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-14">
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-foreground text-balance mb-3">
            Get in Touch
          </h1>
          <p className="text-muted-foreground text-base max-w-lg mx-auto">
            Questions about the tool, collaboration, or just curious about the project?
            We&apos;d love to hear from you.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          <div className="lg:col-span-2 flex flex-col gap-5">
            <div className="rounded-2xl border border-border/60 bg-card p-6">
              <h2 className="font-display font-semibold text-base text-foreground mb-5">
                Contact Details
              </h2>
              <ul className="flex flex-col gap-4">
                {contactDetails.map(({ icon: Icon, label, value, href }) => (
                  <li key={label} className="flex items-start gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-md bg-secondary text-primary mt-0.5">
                      <Icon size={15} />
                    </div>
                    <div>
                      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                        {label}
                      </p>
                      {href ? (
                        <a
                          href={href}
                          target={href.startsWith('http') ? '_blank' : undefined}
                          rel="noopener noreferrer"
                          className="text-sm text-foreground hover:text-accent transition-colors"
                        >
                          {value}
                        </a>
                      ) : (
                        <p className="text-sm text-foreground">{value}</p>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-2xl border border-dashed border-accent/40 bg-accent/5 p-5">
              <p className="text-xs text-muted-foreground leading-relaxed">
                <span className="font-semibold text-foreground">Am I Delusional?</span> was built
                during a hackathon by Team Warlords. We&apos;re open to collaborating, feedback,
                and contributions &mdash; especially from psychology researchers and developers.
              </p>
            </div>
          </div>

          <div className="lg:col-span-3">
            <div className="rounded-2xl border border-border/80 bg-card shadow-sm overflow-hidden">
              <div className="h-1 bg-gradient-to-r from-primary via-accent to-[oklch(0.75_0.1_285)]" />

              {submitted ? (
                <div className="flex flex-col items-center justify-center gap-4 p-12 text-center">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-accent/15 text-accent">
                    <CheckCircle size={28} />
                  </div>
                  <div>
                    <h3 className="font-display font-bold text-lg text-foreground">
                      Message Sent!
                    </h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      Thanks, {form.name}. We&apos;ll get back to you within 24 hours.
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setSubmitted(false)
                      setForm({ name: '', email: '', message: '' })
                    }}
                    className="mt-2"
                  >
                    Send Another
                  </Button>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="p-6 sm:p-8 flex flex-col gap-5">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="flex flex-col gap-1.5">
                      <label htmlFor="name" className="text-sm font-semibold text-foreground">
                        Name
                      </label>
                      <input
                        id="name"
                        name="name"
                        type="text"
                        required
                        value={form.name}
                        onChange={handleChange}
                        placeholder="Your name"
                        className="rounded-lg border border-input bg-background px-3.5 py-2.5 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-ring/60 transition"
                      />
                    </div>
                    <div className="flex flex-col gap-1.5">
                      <label htmlFor="email" className="text-sm font-semibold text-foreground">
                        Email
                      </label>
                      <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        value={form.email}
                        onChange={handleChange}
                        placeholder="you@example.com"
                        className="rounded-lg border border-input bg-background px-3.5 py-2.5 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-ring/60 transition"
                      />
                    </div>
                  </div>

                  <div className="flex flex-col gap-1.5">
                    <label htmlFor="message" className="text-sm font-semibold text-foreground">
                      Message
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      rows={5}
                      required
                      value={form.message}
                      onChange={handleChange}
                      placeholder="Tell us about your feedback, question, or collaboration idea..."
                      className="resize-none rounded-lg border border-input bg-background px-3.5 py-2.5 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-ring/60 transition leading-relaxed"
                    />
                  </div>

                  <Button
                    type="submit"
                    size="lg"
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold gap-2"
                  >
                    <Send size={16} />
                    Send Message
                  </Button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
