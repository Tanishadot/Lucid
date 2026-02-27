import React from 'react';
import { motion } from 'framer-motion';
import { fadeIn } from '../animations/animationVariants';

const Disclaimer: React.FC = () => {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={fadeIn}
      className="py-12 px-4 mt-8"
    >
      <div className="max-w-4xl mx-auto">
        <div className="lucid-card p-6 md:p-8">
          <div className="text-center">
            <h3 className="text-lg font-medium lucid-secondary-text mb-4">Disclaimer</h3>
            
            <div className="text-sm lucid-muted-text space-y-4 leading-relaxed">
              <p>
                LUCID is a reflection-based AI companion designed to support thoughtful reflection and clarity. 
                It does not provide medical, psychological, legal, or crisis intervention services.
              </p>
              
              <p>
                If you are experiencing severe emotional distress, thoughts of self-harm, or a mental health emergency, 
                please seek professional help immediately.
              </p>
              
              <div className="mt-6">
                <h4 className="text-base font-medium lucid-primary-text mb-3">India – Emergency & Mental Health Helplines:</h4>
                <div className="space-y-2 text-left max-w-2xl mx-auto">
                  <div className="flex items-start space-x-2">
                    <span className="lucid-secondary-text mt-1">•</span>
                    <div>
                      <span className="lucid-primary-text font-medium">KIRAN Mental Health Rehabilitation Helpline:</span>
                      <span className="lucid-muted-text"> 1800-599-0019 (24/7, Government of India)</span>
                    </div>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="lucid-secondary-text mt-1">•</span>
                    <div>
                      <span className="lucid-primary-text font-medium">AASRA Suicide Prevention Helpline:</span>
                      <span className="lucid-muted-text"> +91-9820466726 (24/7)</span>
                    </div>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="lucid-secondary-text mt-1">•</span>
                    <div>
                      <span className="lucid-primary-text font-medium">Emergency Services:</span>
                      <span className="lucid-muted-text"> 112</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <p className="mt-6">
                If you are outside India, please contact your local emergency number or a licensed mental health professional in your region.
              </p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Disclaimer;
