import { useEffect, useRef, useState } from 'react';

interface ParallaxOptions {
  speed?: number; // 0.1 to 1.0, where 0.1 is slowest
  enabled?: boolean;
}

export const useParallaxScroll = (options: ParallaxOptions = {}) => {
  const { speed = 0.3, enabled = true } = options;
  const elementRef = useRef<HTMLElement>(null);
  const [scrollY, setScrollY] = useState(0);
  const rafRef = useRef<number>();

  useEffect(() => {
    if (!enabled) return;

    let ticking = false;
    
    const updateScrollY = () => {
      setScrollY(window.scrollY);
      ticking = false;
    };

    const handleScroll = () => {
      if (!ticking) {
        rafRef.current = requestAnimationFrame(updateScrollY);
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, [enabled]);

  const transform = scrollY * speed;
  
  return {
    elementRef,
    transform,
    style: {
      transform: `translate3d(0, ${transform}px, 0)`,
      willChange: 'transform',
      backfaceVisibility: 'hidden' as const,
      perspective: '1000px',
    }
  };
};
