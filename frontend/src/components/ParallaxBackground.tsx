import React from 'react';
import { useParallaxScroll } from '../hooks/useParallaxScroll';

interface ParallaxBackgroundProps {
  children?: React.ReactNode;
  speed?: number;
  className?: string;
}

const ParallaxBackground: React.FC<ParallaxBackgroundProps> = ({ 
  children, 
  speed = 0.25, 
  className = "" 
}) => {
  const { style: parallaxStyle } = useParallaxScroll({ speed });

  return (
    <div 
      className={`absolute inset-0 pointer-events-none parallax-element ${className}`}
      style={parallaxStyle}
    >
      {children}
    </div>
  );
};

export default ParallaxBackground;
