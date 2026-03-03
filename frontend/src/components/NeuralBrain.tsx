import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

interface Node {
  id: number;
  x: number;
  y: number;
  z: number;
  size: number;
  connections: number[];
  pulsePhase: number;
}

interface Connection {
  from: number;
  to: number;
  active: boolean;
  progress: number;
}

const NeuralBrain: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const nodesRef = useRef<Node[]>([]);
  const connectionsRef = useRef<Connection[]>([]);
  const mouseRef = useRef({ x: 0, y: 0 });
  const animationRef = useRef<number>();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize nodes in a brain-like shape
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const nodeCount = 80;
    const nodes: Node[] = [];

    // Create brain hemisphere distribution
    for (let i = 0; i < nodeCount; i++) {
      const angle = Math.random() * Math.PI * 2;
      const radius = 80 + Math.random() * 200;
      const heightVariation = (Math.random() - 0.5) * 150;
      
      // Create two hemispheres
      const hemisphere = i < nodeCount / 2 ? -1 : 1;
      const x = centerX + hemisphere * (Math.abs(Math.cos(angle)) * radius * 0.8) + (Math.random() - 0.5) * 100;
      const y = centerY + Math.sin(angle) * radius * 0.6 + heightVariation;
      const z = (Math.random() - 0.5) * 100;

      const size = 2 + Math.random() * 3;
      
      nodes.push({
        id: i,
        x,
        y,
        z,
        size,
        connections: [],
        pulsePhase: Math.random() * Math.PI * 2
      });
    }

    // Create connections between nearby nodes
    const connections: Connection[] = [];
    nodes.forEach((node, i) => {
      nodes.forEach((other, j) => {
        if (i >= j) return;
        const distance = Math.hypot(node.x - other.x, node.y - other.y);
        if (distance < 120 && Math.random() > 0.6) {
          node.connections.push(j);
          other.connections.push(i);
          connections.push({
            from: i,
            to: j,
            active: false,
            progress: 0
          });
        }
      });
    });

    nodesRef.current = nodes;
    connectionsRef.current = connections;
    setIsLoaded(true);

    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current = { x: e.clientX, y: e.clientY };
    };
    window.addEventListener('mousemove', handleMouseMove);

    let time = 0;
    const animate = () => {
      time += 0.016;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const mouseX = mouseRef.current.x;
      const mouseY = mouseRef.current.y;

      // Draw connections
      connectionsRef.current.forEach((conn, idx) => {
        const fromNode = nodesRef.current[conn.from];
        const toNode = nodesRef.current[conn.to];

        // Parallax effect based on mouse
        const parallaxX = (mouseX - centerX) * 0.02;
        const parallaxY = (mouseY - centerY) * 0.02;

        const fromX = fromNode.x - parallaxX * (1 + fromNode.z / 100);
        const fromY = fromNode.y - parallaxY * (1 + fromNode.z / 100);
        const toX = toNode.x - parallaxX * (1 + toNode.z / 100);
        const toY = toNode.y - parallaxY * (1 + toNode.z / 100);

        // Randomly activate connections
        if (!conn.active && Math.random() < 0.005) {
          conn.active = true;
          conn.progress = 0;
        }

        if (conn.active) {
          conn.progress += 0.03;
          if (conn.progress >= 1) {
            conn.active = false;
            conn.progress = 0;
          }
        }

        const gradient = ctx.createLinearGradient(fromX, fromY, toX, toY);
        
        if (conn.active) {
          const pulsePos = conn.progress;
          gradient.addColorStop(0, 'rgba(176, 75, 163, 0.1)');
          gradient.addColorStop(Math.max(0, pulsePos - 0.2), 'rgba(124, 92, 255, 0.3)');
          gradient.addColorStop(pulsePos, 'rgba(176, 75, 163, 0.8)');
          gradient.addColorStop(Math.min(1, pulsePos + 0.2), 'rgba(124, 92, 255, 0.3)');
          gradient.addColorStop(1, 'rgba(176, 75, 163, 0.1)');
        } else {
          gradient.addColorStop(0, `rgba(156, 134, 216, ${0.4})`);
          gradient.addColorStop(0.5, `rgba(156, 134, 216, ${0.2})`);
          gradient.addColorStop(1, 'rgba(156, 134, 216, 0)');
        }

        ctx.beginPath();
        ctx.moveTo(fromX, fromY);
        ctx.lineTo(toX, toY);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = conn.active ? 2 : 0.5;
        ctx.stroke();
      });

      // Draw nodes
      nodesRef.current.forEach((node) => {
        const parallaxX = (mouseX - centerX) * 0.02;
        const parallaxY = (mouseY - centerY) * 0.02;
        const x = node.x - parallaxX * (1 + node.z / 100);
        const y = node.y - parallaxY * (1 + node.z / 100);

        // Pulsing effect
        const pulse = Math.sin(time * 2 + node.pulsePhase) * 0.3 + 0.7;
        const size = node.size * pulse;

        // Glow effect
        const glowSize = size * 4;
        const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, glowSize);
        glowGradient.addColorStop(0, `rgba(156, 134, 216, ${0.4 * pulse})`);
        glowGradient.addColorStop(0.5, `rgba(236, 72, 153, ${0.2 * pulse})`);
        glowGradient.addColorStop(1, 'transparent');

        ctx.beginPath();
        ctx.arc(x, y, glowSize, 0, Math.PI * 2);
        ctx.fillStyle = glowGradient;
        ctx.fill();

        // Node color
        const nodeGradient = ctx.createRadialGradient(x, y, 0, x, y, node.size * 2);
        nodeGradient.addColorStop(0, `rgba(156, 134, 216, ${pulse})`);
        nodeGradient.addColorStop(0.5, `rgba(156, 134, 216, ${pulse * 0.5})`);
        nodeGradient.addColorStop(1, 'rgba(156, 134, 216, 0)');

        // Core node
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${0.8 + pulse * 0.2})`;
        ctx.fill();
      });

      // Subtle brain rotation
      const rotation = Math.sin(time * 0.3) * 0.02;
      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(rotation);
      ctx.translate(-centerX, -centerY);
      ctx.restore();

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      window.removeEventListener('mousemove', handleMouseMove);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return (
    <div className="relative w-full h-full overflow-hidden">
      <canvas
        ref={canvasRef}
        className="absolute inset-0 z-0"
        style={{ opacity: isLoaded ? 1 : 0, transition: 'opacity 1s ease' }}
      />
      
      {/* Ambient glow behind brain */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 40%, transparent 70%)',
          filter: 'blur(40px)'
        }}
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.5, 0.8, 0.5]
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: 'easeInOut'
        }}
      />
    </div>
  );
};

export default NeuralBrain;
