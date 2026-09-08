export default function KnowledgePage() {
  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">Knowledge Base</h2>
        <p className="text-muted-foreground mt-1">Access company policies, IT guides, and documentation.</p>
      </div>

      <div className="bg-surface border border-border rounded-xl p-12 text-center text-muted-foreground flex flex-col items-center">
        <p className="text-lg font-medium text-foreground">Coming Soon</p>
        <p className="mt-2 text-sm">The employee knowledge base is currently under construction.</p>
      </div>
    </div>
  );
}
