import { Trophy, Cpu, Database, FileCode2, Layers, User } from 'lucide-react'

const techStack = [
  {
    icon: Cpu,
    name: 'Kohaku & Semaphore',
    description:
      "Privacy focused WEB3 technologies integrated into the app to ensure your privacy is protected. Anonymising technologies implimented.",
  },
  {
    icon: Layers,
    name: 'LangChain',
    description:
      'Orchestrates the RAG pipeline — chunking, embedding, retrieval, and prompt chaining — for end-to-end clinical analysis.',
  },
  {
    icon: Database,
    name: 'Pinecone Vector DB',
    description:
      'Stores and retrieves psychology literature embeddings at scale, enabling context-aware RAG for accurate diagnoses.',
  },
  {
    icon: FileCode2,
    name: 'ReportLab',
    description:
      'Generates professional, structured PDF reports with clinical scores, charts, and personalized recommendations.',
  },
]

const teamMembers = [
  {
    name: 'Vansh Aggarwal',
    role: 'Lead Developer',
    initials: 'VA',
    gradient: 'from-[oklch(0.38_0.14_265)] to-[oklch(0.52_0.16_265)]',
  },
  {
    name: 'Team Warlords',
    role: 'Hackathon Team',
    initials: 'TW',
    gradient: 'from-[oklch(0.65_0.14_186)] to-[oklch(0.52_0.16_186)]',
  },
]

export const metadata = {
  title: 'About — Am I Delusional?',
  description:
    'Meet the team and learn about the mission behind Am I Delusional?, built by Vansh Aggarwal and Team Warlords at a hackathon.',
}

export default function AboutPage() {
  return (
    <main className="py-16">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full bg-secondary px-3 py-1 text-xs font-medium text-primary mb-4">
            <Trophy size={12} />
            Hackathon Project
          </div>
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-foreground text-balance mb-4">
            About Am I Delusional?
          </h1>
          <p className="text-muted-foreground text-base leading-relaxed max-w-2xl mx-auto">
            Built at a hackathon by Team Warlords &mdash; a clinical-grade AI tool that brings
            behavioral psychology into everyday relationship conversations.
          </p>
        </div>

        <section className="mb-16">
          <div className="rounded-2xl border border-border/60 bg-card overflow-hidden">
            <div className="h-1 bg-gradient-to-r from-primary via-accent to-[oklch(0.75_0.1_285)]" />
            <div className="p-8 sm:p-10">
              <h2 className="font-display text-2xl font-bold text-foreground mb-4">Our Mission</h2>
              <div className="flex flex-col gap-4 text-muted-foreground text-base leading-relaxed">
                <p>
                  Relationship health is one of the strongest predictors of overall wellbeing &mdash; yet
                  most people have no objective way to assess the dynamics of their own
                  relationships. Therapists are expensive and inaccessible; friends are biased.
                </p>
                <p>
                  <span className="text-foreground font-medium">Am I Delusional?</span> bridges
                  that gap. Using your WhatsApp chat history as a behavioral dataset, our AI applies
                  proven clinical frameworks &mdash; Gottman&apos;s Four Horsemen, Attachment Theory,
                  and Cognitive Behavioral principles &mdash; to score your relationship across key dimensions.
                </p>
                <p>
                  We built this specifically for{' '}
                  <span className="text-foreground font-medium">Indian relationships</span>{' '}
                  because the cultural context matters deeply. The model is trained to understand
                  family pressure dynamics, implicit communication styles, and nuances unique to the
                  Indian relationship experience.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="mb-16">
          <div className="text-center mb-10">
            <h2 className="font-display text-2xl font-bold text-foreground">
              Clinical-Grade Architecture
            </h2>
            <p className="mt-2 text-muted-foreground text-sm">
              Built with a production-ready AI stack, not just a wrapper.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {techStack.map(({ icon: Icon, name, description }) => (
              <div
                key={name}
                className="flex gap-4 rounded-xl border border-border/60 bg-card p-5 hover:border-accent/40 hover:shadow-sm transition-all"
              >
                <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-secondary text-primary">
                  <Icon size={18} />
                </div>
                <div>
                  <h3 className="font-display font-semibold text-sm text-foreground mb-1">{name}</h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">{description}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 rounded-xl border border-border/60 bg-muted/40 px-6 py-4">
            <p className="text-sm text-muted-foreground leading-relaxed text-center">
              <span className="font-medium text-foreground">Custom RAG pipeline</span> &mdash; psychology
              research papers and clinical literature are embedded into Pinecone, enabling the model
              to ground every diagnosis in established academic frameworks. Local LLM fine-tuning
              ensures culturally-aware outputs.
            </p>
          </div>
        </section>

        <section>
          <div className="text-center mb-10">
            <h2 className="font-display text-2xl font-bold text-foreground">Meet the Team</h2>
          </div>

          <div className="flex flex-col sm:flex-row gap-5 justify-center">
            {teamMembers.map(({ name, role, initials, gradient }) => (
              <div
                key={name}
                className="flex flex-col items-center gap-4 rounded-2xl border border-border/60 bg-card p-8 flex-1"
              >
                <div
                  className={`flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br ${gradient} text-white font-display font-bold text-xl shadow`}
                >
                  {initials}
                </div>
                <div className="text-center">
                  <p className="font-display font-semibold text-base text-foreground">{name}</p>
                  <p className="text-sm text-muted-foreground mt-0.5">{role}</p>
                </div>
              </div>
            ))}

            <div className="flex flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-accent/50 bg-accent/5 p-8 flex-1">
              <User size={28} className="text-accent" />
              <div className="text-center">
                <p className="font-display font-semibold text-base text-foreground">Built in 200 hr sprint</p>
                <p className="text-sm text-muted-foreground mt-0.5">Hackathon Sprint</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}
