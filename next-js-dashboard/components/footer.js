import Link from 'next/link'
import { Brain, ExternalLink, Mail, Heart } from 'lucide-react'

const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'Try Tool', href: '/tool' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
]

const techStack = [ 'Python 3', 'JavaScript', 'Next.JS', 'Kohaku', 'Semaphore', 'Custom AI', 'LangChain', 'Pinecone Vector DB', 'ReportLab (PDF)','Caspian SDK']

export function Footer() {
  return (
    <footer className="border-t border-border/60 bg-card">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-3">
          {/* Brand */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2.5">
              <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground">
                <Brain size={14} />
              </div>
              <span className="font-display font-semibold text-sm text-foreground">
                Am I Delusional?
              </span>
            </div>
            <p className="text-xs leading-relaxed text-muted-foreground max-w-[220px]">
              Clinical AI-powered relationship diagnostics built for Indian relationships. Privacy built on Web3 technology with Ethereum based encryption for maximum privacy.
            </p>
            <div className="flex items-center gap-3 mt-1">
              <a
                href="https://github.com/itswarlord/amidelusional"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-foreground transition-colors"
                aria-label="GitHub"
              >
                <ExternalLink size={16} />
              </a>
              <a
                href="mailto:vansh@iitg.ac.in"
                className="text-muted-foreground hover:text-foreground transition-colors"
                aria-label="Email"
              >
                <Mail size={16} />
              </a>
            </div>
          </div>

          {/* Navigation */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">
              Navigation
            </h3>
            <ul className="flex flex-col gap-2.5">
              {navLinks.map(({ label, href }) => (
                <li key={href}>
                  <Link
                    href={href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Built with */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">
              Powered by
            </h3>
            <ul className="flex flex-col gap-2.5 text-sm text-muted-foreground">
              {techStack.map((tech) => (
                <li key={tech}>{tech}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-border/60 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()} Am I Delusional? &mdash; Team Warlords
          </p>
          <p className="text-xs text-muted-foreground flex items-center gap-1">
            Made with <Heart size={15} className="text-accent fill-accent" /> by Vansh Aggarwal. Credit Vercel APP for template.
          </p>
        </div>
      </div>
    </footer>
  )
}
