'use client'

import { useState, useRef, useCallback } from 'react'
import {
  UploadCloud,
  FileText,
  CheckCircle,
  Download,
  Loader2,
  X,
  Sparkles,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

export default function ToolPage() {
  const [background, setBackground] = useState('')
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [pdfUrl, setPdfUrl] = useState('') // Added state for the PDF link
  const fileInputRef = useRef(null)

  const handleFile = (f) => {
    if (f.name.endsWith('.txt')) {
      setFile(f)
    } else {
      alert('Please upload a .txt file.')
    }
  }

  const onDrop = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped) handleFile(dropped)
  }, [])

  const onDragOver = useCallback((e) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const onDragLeave = useCallback(() => setIsDragging(false), [])

  const handleInputChange = (e) => {
    const f = e.target.files?.[0]
    if (f) handleFile(f)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    
    setIsGenerating(true)
    setIsSuccess(false)
    setPdfUrl('')

    // Package the file and background text
    const formData = new FormData()
    formData.append('background', background)
    formData.append('chat_file', file)

    try {
      // Pointing to your local Python FastAPI server
      const response = await fetch('http://34.14.222.173:8000/api/analyze', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to connect to the backend server.')
      }

      const data = await response.json()

      if (data.status === 'success') {
        setPdfUrl(data.download_url)
        setIsSuccess(true)
      } else {
        throw new Error(data.detail || 'Analysis failed.')
      }
    } catch (error) {
      console.error('Error analyzing chat:', error)
      alert('Something went wrong. Make sure your Python backend is running on port 8000.')
    } finally {
      setIsGenerating(false)
    }
  }

  const reset = () => {
    setFile(null)
    setIsSuccess(false)
    setBackground('')
    setPdfUrl('')
  }

  return (
    <main className="py-16">
      <div className="mx-auto max-w-2xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 rounded-full bg-secondary px-3 py-1 text-xs font-medium text-primary mb-4">
            <Sparkles size={12} />
            AI-Powered Clinical Analysis
          </div>
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-foreground text-balance">
            Relationship Diagnostic Tool
          </h1>
          <p className="mt-3 text-muted-foreground text-base leading-relaxed">
            Upload your WhatsApp chat export and provide context. Our AI will generate a
            clinical-grade PDF report in seconds.
          </p>
        </div>

        <div className="rounded-2xl border border-border/80 bg-card shadow-sm overflow-hidden">
          <div className="h-1 w-full bg-gradient-to-r from-primary via-accent to-[oklch(0.75_0.1_285)]" />

          <form onSubmit={handleSubmit} className="p-6 sm:p-8 flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <label htmlFor="background" className="text-sm font-semibold text-foreground">
                Background Context
              </label>
              <textarea
                id="background"
                rows={5}
                value={background}
                onChange={(e) => setBackground(e.target.value)}
                placeholder="Tell us a bit about your relationship, ages, how you met, how long you've been together, any recurring issues..."
                className="w-full resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-ring/60 transition leading-relaxed"
              />
              <p className="text-xs text-muted-foreground">
                More context = more accurate diagnosis. Share freely &mdash; nothing is stored.
              </p>
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-foreground">
                WhatsApp Chat Export (.txt)
              </label>

              {file ? (
                <div className="flex items-center gap-3 rounded-lg border border-accent/40 bg-accent/5 px-4 py-3">
                  <FileText size={18} className="text-accent flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{file.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB &mdash; ready to analyze
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setFile(null)}
                    className="text-muted-foreground hover:text-foreground transition-colors flex-shrink-0"
                    aria-label="Remove file"
                  >
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <div
                  onClick={() => fileInputRef.current?.click()}
                  onDrop={onDrop}
                  onDragOver={onDragOver}
                  onDragLeave={onDragLeave}
                  role="button"
                  tabIndex={0}
                  aria-label="Upload WhatsApp chat export file"
                  onKeyDown={(e) => e.key === 'Enter' && fileInputRef.current?.click()}
                  className={cn(
                    'relative flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-10 cursor-pointer transition-all',
                    isDragging
                      ? 'border-accent bg-accent/8 scale-[1.01]'
                      : 'border-border/80 bg-muted/40 hover:border-primary/50 hover:bg-secondary/40'
                  )}
                >
                  <UploadCloud
                    size={36}
                    className={cn(
                      'transition-colors',
                      isDragging ? 'text-accent' : 'text-muted-foreground'
                    )}
                  />
                  <div className="text-center">
                    <p className="text-sm font-medium text-foreground">
                      Drop your .txt file here, or{' '}
                      <span className="text-accent underline underline-offset-2">browse</span>
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      WhatsApp &rarr; Chat &rarr; Export Chat &rarr; Without Media &rarr; .txt file
                    </p>
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".txt"
                    onChange={handleInputChange}
                    className="sr-only"
                    aria-hidden="true"
                  />
                </div>
              )}
            </div>

            <Button
              type="submit"
              disabled={!file || isGenerating}
              size="lg"
              className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-base gap-2 disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  Generating Clinical Report...
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  Generate Clinical Report
                </>
              )}
            </Button>
          </form>

          {isSuccess && (
            <div className="mx-6 mb-6 sm:mx-8 rounded-xl border border-accent/30 bg-accent/8 px-5 py-5">
              <div className="flex items-start gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-accent/15 text-accent flex-shrink-0">
                  <CheckCircle size={20} />
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-foreground text-sm">Report Generated!</p>
                  <p className="text-xs text-muted-foreground mt-0.5 mb-3">
                    Your clinical PDF report is ready. It contains relationship scores,
                    behavioral pattern analysis, and actionable insights.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-2">
                    {/* The Button is now wired up to download the PDF URL */}
                    <Button
                      asChild
                      size="sm"
                      className="gap-2 bg-accent hover:bg-accent/90 text-accent-foreground"
                    >
                      <a href={pdfUrl} target="_blank" rel="noopener noreferrer">
                        <Download size={15} />
                        Your PDF Report is Ready
                      </a>
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={reset}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      Analyze Another
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <p className="mt-5 text-center text-xs text-muted-foreground/60 leading-relaxed">
          Your data is analyzed locally and never stored or shared. This tool is for informational
          purposes and does not replace professional therapy.
        </p>
      </div>
    </main>
  )
}