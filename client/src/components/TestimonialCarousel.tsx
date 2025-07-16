import React, { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { FormatQuote, ArrowBackIosNew, ArrowForwardIos } from '@mui/icons-material';

const ArrowButton = ({ onClick, disabled, children }: { onClick: () => void; disabled: boolean; children: React.ReactNode }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className="absolute top-1/2 -translate-y-1/2 bg-slate-700/50 hover:bg-slate-700/80 disabled:opacity-30 transition-all rounded-full p-2 text-white z-10"
  >
    {children}
  </button>
);

const testimonials = [
  {
    quote: "This tool has revolutionized my content workflow. I'm saving at least 10 hours a week. Incredible!",
    author: "Sarah J.",
    role: "Marketing Manager"
  },
  {
    quote: "+I love how it generates platform-specific content. My engagement rates have skyrocketed since I started using Post GenerAItor.",
    author: "Oliver T.",
    role: "Key Account Creator"
  },
  {
    quote: "Post GenerAItor has completely transformed the way we create content. It's like having a personal writing assistant.",
    author: "Micaela V.",
    role: "Head of Strategy"
  },
  {
    quote: "I've tried many AI writing tools, but this one stands out. The quality is exceptional and the interface is so user-friendly.",
    author: "Courtney R.",
    role: "Drafting Specialist"
  },
  {
    quote: "Post GenerAItor has been a lifesaver for our team. The ability to generate high-quality content quickly has improved our workflow immensely.",
    author: "Marco S.",
    role: "Leading Content Creator"
  },
  {
    quote: "As a freelance content creator, Post GenerAItor is a game-changer. The quality of the generated text is top-notch and requires minimal editing.",
    author: "Alex D.",
    role: "Content Creator"
  },
  {
    quote: "I was skeptical about AI writers, but this one is different. It perfectly captures the tone for different social media platforms.",
    author: "Maria K.",
    role: "Social Media Strategist"
  },
    {
    quote: "The ability to generate content for my blog and X feed from a single idea is just brilliant. Highly recommended for any blogger.",
    author: "David L.",
    role: "Tech Blogger"
  }
];

const TestimonialCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true, align: 'start' });

  const [prevBtnDisabled, setPrevBtnDisabled] = useState(true);
  const [nextBtnDisabled, setNextBtnDisabled] = useState(true);

  const scrollPrev = useCallback(() => emblaApi && emblaApi.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi && emblaApi.scrollNext(), [emblaApi]);

  useEffect(() => {
    if (!emblaApi) {
      return;
    }

    const onSelect = () => {
      // With loop: true, these will always be true, but it's good practice to have this logic.
      setPrevBtnDisabled(!emblaApi.canScrollPrev());
      setNextBtnDisabled(!emblaApi.canScrollNext());
    };
    
    emblaApi.on('select', onSelect);
    emblaApi.on('reInit', onSelect);
    onSelect(); // Set initial state

    // Cleanup listener on unmount
    return () => {
      emblaApi.off('select', onSelect);
      emblaApi.off('reInit', onSelect);
    };
  }, [emblaApi]);


  return (
    // We add 'relative' to this container to position our absolute arrows inside it.
    <div className="relative">
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex">
          {testimonials.map((testimonial, index) => (
            // --- MODIFICATION for peeking next slide ---
            // On small screens, we use 'basis-11/12' instead of 'basis-full'.
            // This makes the slide slightly smaller than the container, revealing the next one.
            <div className="flex-grow-0 flex-shrink-0 basis-11/12 md:basis-1/2 lg:basis-1/3 min-w-0 pl-4" key={index}>
              <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 h-full flex flex-col">
                <FormatQuote className="text-cyan-400 !h-16 !w-16 -mt-4 -ml-4 mb-2" />
                <p className="text-slate-300 italic mb-6 flex-grow">"{testimonial.quote}"</p>
                <div>
                  <p className="font-bold text-lg text-slate-100">{testimonial.author}</p>
                  <p className="text-violet-400">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* --- ADDED ARROW BUTTONS --- */}
      <div className="hidden md:block">
        <ArrowButton onClick={scrollPrev} disabled={prevBtnDisabled}><ArrowBackIosNew className="ml-2" /></ArrowButton>
        <ArrowButton onClick={scrollNext} disabled={nextBtnDisabled}><ArrowForwardIos /></ArrowButton>
      </div>
      
      {/* We need to style the arrows slightly differently for correct positioning */}
      <style>{`
        .hidden.md\\:block > button:first-of-type { left: 0px; transform: translate(-50%, -50%); }
        .hidden.md\\:block > button:last-of-type { right: 0px; transform: translate(50%, -50%); }
      `}</style>
    </div>
  );
};

export default TestimonialCarousel;