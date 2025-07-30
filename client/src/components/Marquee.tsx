const MarqueeItem = ({ children }: { children: React.ReactNode }) => (
  <div className="flex-shrink-0 mx-4 text-xl font-semibold text-slate-300 flex items-center">
    <span className="mr-3 text-cyan-400"></span>
    {children}
  </div>
);

const Marquee = () => {
  const items = [
    "Powered by Cutting-Edge AI",
    "Blog Posts in Seconds",
    "Engaging Social Media Content",
    "Boost Your Productivity",
    "Save Hours of Work",
  ];

  return (
    <div className="relative flex overflow-hidden py-4 border-y border-slate-800 bg-slate-800/20">
      <div className="animate-marquee whitespace-nowrap flex">
        {/* Render items twice for a seamless loop */}
        {items.map((item, index) => <MarqueeItem key={index}>{item}</MarqueeItem>)}
        {items.map((item, index) => <MarqueeItem key={`dup-${index}`}>{item}</MarqueeItem>)}
      </div>
    </div>
  );
};

export default Marquee;