import React, { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';

const BackgroundLayer: React.FC = () => {
  const [isDark, setIsDark] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const particlesRef = useRef<Array<{
    x: number;
    y: number;
    vx: number;
    vy: number;
    size: number;
    opacity: number;
    pulsePhase: number;
  }>>([]);

  useEffect(() => {
    // Check if dark mode is active
    const checkDarkMode = () => {
      setIsDark(document.documentElement.classList.contains('dark'));
    };
    
    checkDarkMode();
    
    // Listen for theme changes
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
    
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize particles
    const particleCount = 50;
    particlesRef.current = Array.from({ length: particleCount }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.2,
      vy: (Math.random() - 0.5) * 0.2,
      size: Math.random() * 2 + 1,
      opacity: isDark ? 0.45 : 0.35,
      pulsePhase: Math.random() * Math.PI * 2
    }));

    // Neural network connections
    const drawNeuralConnections = () => {
      const maxDistance = 150;
      
      for (let i = 0; i < particlesRef.current.length; i++) {
        for (let j = i + 1; j < particlesRef.current.length; j++) {
          const p1 = particlesRef.current[i];
          const p2 = particlesRef.current[j];
          const distance = Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
          
          if (distance < maxDistance) {
            const baseOpacity = isDark ? 0.12 : 0.12;
            const opacity = Math.min((1 - distance / maxDistance) * baseOpacity, 0.15);
            ctx.strokeStyle = isDark 
              ? `rgba(180,200,255,${opacity})`
              : `rgba(26,34,56,${opacity})`;
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      }
    };

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update and draw particles
      particlesRef.current.forEach((particle) => {
        // Update position
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.pulsePhase += 0.001; // Slow pulse

        // Wrap around edges
        if (particle.x < 0) particle.x = canvas.width;
        if (particle.x > canvas.width) particle.x = 0;
        if (particle.y < 0) particle.y = canvas.height;
        if (particle.y > canvas.height) particle.y = 0;

        // Calculate pulse scale
        const pulseScale = 1 + Math.sin(particle.pulsePhase) * 0.05;
        const currentSize = particle.size * pulseScale;

        // Draw node with glow
        const nodeColor = isDark 
          ? `rgba(200,220,255,${particle.opacity})`
          : `rgba(26,34,56,${particle.opacity})`;
        
        // Outer glow
        ctx.shadowColor = isDark 
          ? 'rgba(120,140,255,0.4)'
          : 'rgba(120,140,255,0.3)';
        ctx.shadowBlur = 8;
        
        // Draw node
        ctx.fillStyle = nodeColor;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, currentSize, 0, Math.PI * 2);
        ctx.fill();
        
        // Reset shadow for next element
        ctx.shadowColor = 'transparent';
        ctx.shadowBlur = 0;
      });

      // Draw neural connections
      drawNeuralConnections();

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isDark]);

  return (
    <div className="fixed inset-0 pointer-events-none z-[-10]">
      {/* Base gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-blue-950 dark:to-purple-950" />
      
      {/* Center glow field */}
      <div 
        className="absolute inset-0 opacity-80"
        style={{
          background: isDark 
            ? 'radial-gradient(circle at 70% 30%, rgba(120,140,255,0.12) 0%, transparent 50%)'
            : 'radial-gradient(circle at 70% 30%, rgba(120,140,255,0.08) 0%, transparent 50%)',
        }}
      />
      
      {/* Grid layer */}
      <div 
        className="absolute inset-0 opacity-80"
        style={{
          backgroundImage: `
            linear-gradient(to right, currentColor 1px, transparent 1px),
            linear-gradient(to bottom, currentColor 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
          backgroundPosition: '-1px -1px',
          color: isDark ? 'rgba(180,200,255,0.08)' : 'rgba(26,34,56,0.06)',
          mixBlendMode: isDark ? 'soft-light' : 'overlay',
        }}
      />
      
      {/* Animated gradient overlay */}
      <motion.div
        className="absolute inset-0 opacity-30"
        animate={{
          background: [
            'radial-gradient(circle at 20% 50%, rgba(147, 197, 253, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 80% 50%, rgba(165, 180, 252, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 50% 20%, rgba(196, 181, 253, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 20% 50%, rgba(147, 197, 253, 0.3) 0%, transparent 50%)',
          ]
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* Canvas for particles and neural connections */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        style={{
          mixBlendMode: isDark ? 'soft-light' : 'overlay',
        }}
      />
      
      {/* Floating light beams with enhanced visibility */}
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-px h-full bg-gradient-to-b from-transparent via-blue-400/30 to-transparent"
          style={{
            left: `${20 + i * 30}%`,
            mixBlendMode: isDark ? 'soft-light' : 'overlay',
          }}
          animate={{
            x: [0, 100, 0],
            opacity: [0.2, 0.4, 0.2],
          }}
          transition={{
            duration: 20 + i * 5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: i * 2,
          }}
        />
      ))}
    </div>
  );
};

export default BackgroundLayer;
