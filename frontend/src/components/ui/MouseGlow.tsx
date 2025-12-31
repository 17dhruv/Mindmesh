'use client';

import React, { useEffect, useRef, useState } from 'react';

export function MouseGlow() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const requestRef = useRef<number>();
  const mouseRef = useRef({ x: 0, y: 0 });
  const currentRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current = {
        x: e.clientX,
        y: e.clientY
      };
    };

    // Smooth animation loop
    const animate = () => {
      // Smooth interpolation (lerp)
      const ease = 0.1;
      currentRef.current.x += (mouseRef.current.x - currentRef.current.x) * ease;
      currentRef.current.y += (mouseRef.current.y - currentRef.current.y) * ease;

      setMousePosition({
        x: currentRef.current.x,
        y: currentRef.current.y
      });

      requestRef.current = requestAnimationFrame(animate);
    };

    requestRef.current = requestAnimationFrame(animate);

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, []);

  return (
    <>
      {/* Primary glow - follows mouse with purple/pink gradient */}
      <div
        className="fixed pointer-events-none transition-opacity duration-500 opacity-100"
        style={{
          left: mousePosition.x,
          top: mousePosition.y,
          transform: 'translate(-50%, -50%)',
          zIndex: 1,
        }}
      >
        {/* Large outer glow */}
        <div
          className="absolute rounded-full blur-3xl"
          style={{
            width: '600px',
            height: '600px',
            background: 'radial-gradient(circle, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.15) 30%, transparent 70%)',
            marginLeft: '-300px',
            marginTop: '-300px',
          }}
        />

        {/* Inner glow */}
        <div
          className="absolute rounded-full blur-2xl"
          style={{
            width: '300px',
            height: '300px',
            background: 'radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, rgba(236, 72, 153, 0.2) 40%, transparent 70%)',
            marginLeft: '-150px',
            marginTop: '-150px',
          }}
        />

        {/* Core glow */}
        <div
          className="absolute rounded-full blur-xl"
          style={{
            width: '150px',
            height: '150px',
            background: 'radial-gradient(circle, rgba(139, 92, 246, 0.4) 0%, rgba(236, 72, 153, 0.3) 50%, transparent 70%)',
            marginLeft: '-75px',
            marginTop: '-75px',
          }}
        />
      </div>

      {/* Secondary trailing glow with cyan accent */}
      <div
        className="fixed pointer-events-none transition-opacity duration-700 opacity-80"
        style={{
          left: mousePosition.x * 0.8,
          top: mousePosition.y * 0.8,
          transform: 'translate(-50%, -50%)',
          zIndex: 0,
        }}
      >
        <div
          className="absolute rounded-full blur-3xl"
          style={{
            width: '400px',
            height: '400px',
            background: 'radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.1) 50%, transparent 70%)',
            marginLeft: '-200px',
            marginTop: '-200px',
          }}
        />
      </div>

      {/* Small sparkle/trail effect */}
      <div
        className="fixed pointer-events-none"
        style={{
          left: mousePosition.x,
          top: mousePosition.y,
          transform: 'translate(-50%, -50%)',
          zIndex: 2,
        }}
      >
        <div className="absolute w-2 h-2 rounded-full blur-sm animate-pulse" style={{ backgroundColor: 'rgba(139, 92, 246, 0.6)' }} />
        <div className="absolute w-3 h-3 rounded-full blur-md animate-pulse" style={{ backgroundColor: 'rgba(236, 72, 153, 0.4)', marginLeft: '-8px', marginTop: '-4px', animationDelay: '0.2s' }} />
        <div className="absolute w-4 h-4 rounded-full blur-lg animate-pulse" style={{ backgroundColor: 'rgba(139, 92, 246, 0.2)', marginLeft: '-16px', marginTop: '-8px', animationDelay: '0.4s' }} />
      </div>
    </>
  );
}
