import { ThemeToggle } from "@/components/ThemeToggle";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, Server, Shield } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="container mx-auto px-4 py-6 flex justify-end">
        <ThemeToggle />
      </header>
      
      <main className="container mx-auto px-4 py-12 max-w-5xl">
        <div className="text-center space-y-4 mb-16">
          <h1 className="text-5xl md:text-7xl font-bold text-foreground">
            LangChain Agent
          </h1>
          <p className="text-xl text-muted-foreground">
            MCP Server
          </p>
        </div>

        {/* Key Features */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold mb-8 text-center">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <Brain className="w-8 h-8 text-primary mb-2" />
                <CardTitle>LangGraph Integration</CardTitle>
                <CardDescription>
                  Built on LangChain/LangGraph for stateful, production-grade agent workflows
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Server className="w-8 h-8 text-primary mb-2" />
                <CardTitle>FastAPI Backend</CardTitle>
                <CardDescription>
                  High-performance Python web framework with automatic OpenAPI documentation
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Shield className="w-8 h-8 text-primary mb-2" />
                <CardTitle>Secure & Scalable</CardTitle>
                <CardDescription>
                  Stateless architecture supporting horizontal scaling and API key authentication
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        {/* System Architecture */}
        <section className="mb-16">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">System Architecture</CardTitle>
              <CardDescription>
                Simple, single-process web application with dual MCP endpoints
              </CardDescription>
            </CardHeader>
            <CardContent className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <h3 className="font-semibold">/mcp/manifest</h3>
                <p className="text-sm text-muted-foreground">
                  Returns static JSON declaring the LangChain agent as an MCP tool
                </p>
                <div className="bg-muted p-3 rounded font-mono text-xs">
                  GET /mcp/manifest
                </div>
              </div>

              <div className="space-y-2">
                <h3 className="font-semibold">/mcp/invoke</h3>
                <p className="text-sm text-muted-foreground">
                  Executes agent with user query and returns structured response
                </p>
                <div className="bg-muted p-3 rounded font-mono text-xs">
                  POST /mcp/invoke
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Success Metrics */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold mb-8 text-center">Success Metrics</h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">P95 Latency</CardTitle>
                <CardDescription>Under 5 seconds</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Uptime Target</CardTitle>
                <CardDescription>99.9% availability</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Error Rate</CardTitle>
                <CardDescription>Less than 0.1%</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">MCP Compliance</CardTitle>
                <CardDescription>100% protocol adherence</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        {/* Technology Stack */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold mb-8 text-center">Technology Stack</h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: "Python 3.11+", desc: "Core Runtime" },
              { name: "FastAPI", desc: "Web Framework" },
              { name: "LangGraph", desc: "Agent Framework" },
              { name: "Docker", desc: "Containerization" }
            ].map((tech) => (
              <Card key={tech.name}>
                <CardHeader>
                  <CardTitle className="text-base">{tech.name}</CardTitle>
                  <CardDescription className="text-sm">{tech.desc}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
