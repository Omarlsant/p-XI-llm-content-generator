import React, { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { FormatQuote, ArrowBackIosNew, ArrowForwardIos } from '@mui/icons-material';

const ArrowButton = ({
  onClick,
  disabled,
  children,
  ariaLabel
}: {
  onClick: () => void;
  disabled: boolean;
  children: React.ReactNode;
  ariaLabel: string;
}) => (
  <button
    type="button"
    onClick={onClick}
    disabled={disabled}
    aria-label={ariaLabel}
    className="absolute top-1/2 -translate-y-1/2 bg-slate-700/70 hover:bg-slate-700 disabled:opacity-30 transition-all rounded-full w-11 h-11 flex items-center justify-center text-white z-10 focus:outline-none focus:ring-2 focus:ring-cyan-400 shadow-md"
  >
    {children}
  </button>
);

const testimonials = [
  {
    quote: "This tool has streamlined my content workflow. I save hours of repetitive formatting across channels. Fantastic experience!",
    author: "Sarah J.",
    role: "Marketing Specialist (Illustrative Persona)"
  },
  {
    quote: "I love how it generates platform-specific content. Audience engagement improved once I started tailoring posts with Content GenerAItor.",
    author: "Oliver T.",
    role: "Account Strategist (Illustrative Persona)"
  },
  {
    quote: "Content GenerAItor simplifies the way we draft cross-platform messaging. It acts like a dependable writing co-pilot.",
    author: "Micaela V.",
    role: "Content Planner (Illustrative Persona)"
  },
  {
    quote: "Among modern AI tools, this one stands out for multimodal integration and clean multi-agent architectural separation.",
    author: "Courtney R.",
    role: "Drafting Specialist (Illustrative Persona)"
  },
  {
    quote: "Content GenerAItor accelerates initial drafts, allowing our creative team to spend more time refining brand nuance.",
    author: "Marco S.",
    role: "Creative Lead (Illustrative Persona)"
  },
  {
    quote: "As a freelance writer, Content GenerAItor provides a great starting point. The platform-adapted outputs need minimal manual polish.",
    author: "Alex D.",
    role: "Freelance Creator (Illustrative Persona)"
  },
  {
    quote: "The distinct tone adjustments between Twitter and LinkedIn are spot on. It respects character limits and style requirements.",
    author: "Maria K.",
    role: "Social Media Strategist (Illustrative Persona)"
  },
  {
    quote: "The ability to generate blog concepts and social snippets from a single prompt is brilliant for maintaining editorial cadence.",
    author: "David L.",
    role: "Tech Writer (Illustrative Persona)"
  }
];

const TestimonialCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true, align: 'start' });

  const [prevBtnDisabled, setPrevBtnDisabled] = useState(false);
  const [nextBtnDisabled, setNextBtnDisabled] = useState(false);

  const scrollPrev = useCallback(() => emblaApi && emblaApi.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi && emblaApi.scrollNext(), [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;

    const onSelect = () => {
      setPrevBtnDisabled(!emblaApi.canScrollPrev());
      setNextBtnDisabled(!emblaApi.canScrollNext());
    };
    
    emblaApi.on('select', onSelect);
    emblaApi.on('reInit', onSelect);
    onSelect();

    return () => {
      emblaApi.off('select', onSelect);
      emblaApi.off('reInit', onSelect);
    };
  }, [emblaApi]);

  return (
    <div className="relative max-w-6xl mx-auto px-4">
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex">
          {testimonials.map((testimonial, index) => (
            <div className="flex-grow-0 flex-shrink-0 basis-11/12 md:basis-1/2 lg:basis-1/3 min-w-0 pl-4" key={index}>
              <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 h-full flex flex-col justify-between shadow-lg">
                <div>
                  <FormatQuote className="text-cyan-400 !h-14 !w-14 -mt-3 -ml-3 mb-2" />
                  <p className="text-slate-300 italic mb-6 leading-relaxed">"{testimonial.quote}"</p>
                </div>
                <div className="border-t border-slate-700/60 pt-4">
                  <p className="font-bold text-lg text-slate-100">{testimonial.author}</p>
                  <p className="text-violet-400 text-sm">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Desktop Arrow Buttons */}
      <div className="hidden md:block">
        <ArrowButton onClick={scrollPrev} disabled={prevBtnDisabled} ariaLabel="Previous testimonial">
          <ArrowBackIosNew fontSize="small" className="ml-1" />
        </ArrowButton>
        <ArrowButton onClick={scrollNext} disabled={nextBtnDisabled} ariaLabel="Next testimonial">
          <ArrowForwardIos fontSize="small" />
        </ArrowButton>
      </div>

      {/* Mobile Controls */}
      <div className="flex justify-center items-center gap-4 mt-6 md:hidden">
        <button
          type="button"
          onClick={scrollPrev}
          disabled={prevBtnDisabled}
          aria-label="Previous testimonial"
          className="bg-slate-700/80 hover:bg-slate-700 disabled:opacity-30 rounded-full w-11 h-11 flex items-center justify-center text-white focus:outline-none focus:ring-2 focus:ring-cyan-400"
        >
          <ArrowBackIosNew fontSize="small" className="ml-1" />
        </button>
        <button
          type="button"
          onClick={scrollNext}
          disabled={nextBtnDisabled}
          aria-label="Next testimonial"
          className="bg-slate-700/80 hover:bg-slate-700 disabled:opacity-30 rounded-full w-11 h-11 flex items-center justify-center text-white focus:outline-none focus:ring-2 focus:ring-cyan-400"
        >
          <ArrowForwardIos fontSize="small" />
        </button>
      </div>
      
      <style>{`
        .hidden.md\\:block > button:first-of-type { left: -16px; }
        .hidden.md\\:block > button:last-of-type { right: -16px; }
      `}</style>
    </div>
  );
};

export default TestimonialCarousel;
