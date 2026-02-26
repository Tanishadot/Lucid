import { Variants, Easing } from 'framer-motion';

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.8, ease: "easeOut" as Easing }
  },
};

export const slideUp: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: (custom: number = 0) => ({
    opacity: 1,
    y: 0,
    transition: { 
      duration: 0.6, 
      delay: custom * 0.1,
      ease: "easeOut" as Easing
    }
  }),
};

export const float = {
  y: [-20, 20, -20],
  x: [-10, 10, -10],
  transition: {
    duration: 10,
    repeat: Infinity,
    ease: "easeInOut" as Easing,
  },
};

export const glow = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.8,
      ease: "easeOut" as Easing,
    },
  },
};
