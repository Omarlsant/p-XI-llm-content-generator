import { 
  HourglassEmpty,
  LightbulbOutlined,
  DynamicFeed,
  ArrowDownward,
  Code,
  FlashOn,
  Palette,
  DataObject,
  CloudQueue
} from '@mui/icons-material';
import TechLogo from '../components/TechLogo';
import photoImg from '../assets/photo.jpg';

const CreatorPhoto = () => (
  <div className="w-48 h-48 bg-gradient-to-br from-cyan-500 to-violet-600 rounded-full mx-auto shadow-lg p-1">
    <img
      src={photoImg}
      alt="Portrait of the creator, Omar Lengua"
      width={192}
      height={192}
      loading="lazy"
      className="w-full h-full object-cover rounded-full"
    />
  </div>
);

const About = () => {
  return (
    <div className="max-w-5xl mx-auto py-16 px-4 space-y-24">

      {/* --- Section 1: The Vision --- */}
      <section className="text-center">
        <h1 className="text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-slate-100 to-slate-400 py-2">
          Beyond the Blank Page
        </h1>
        <p className="mt-4 text-2xl font-semibold text-violet-400">Our Mission and the 'Why' Behind Content GenerAItor</p>
      </section>

      {/* --- Section 2: The Problem --- */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">The Creator's Dilemma</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 text-center flex flex-col justify-between">
            <div>
              <HourglassEmpty className="text-cyan-400 h-16 w-16 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">The Time Sink</h3>
              <p className="text-slate-400">Brainstorming, drafting, and tailoring content for different platforms can consume an entire day's work. Quality content demands significant time investment.</p>
            </div>
            <div className="mt-6 border-t border-slate-700/60 pt-4">
              <p className="text-3xl font-extrabold text-cyan-400">Hours Saved</p>
              <p className="text-slate-400 text-sm mt-1">Reduces repetitive drafting cycles across channels</p>
            </div>
          </div>
          <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 text-center flex flex-col justify-between">
            <div>
              <LightbulbOutlined className="text-cyan-400 h-16 w-16 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">Creative Burnout</h3>
              <p className="text-slate-400">The constant pressure to be original and engaging leads to writer's block. Inspiration is a finite resource that needs to be managed carefully.</p>
            </div>
            <div className="mt-6 border-t border-slate-700/60 pt-4">
              <p className="text-3xl font-extrabold text-cyan-400">Creative Flow</p>
              <p className="text-slate-400 text-sm mt-1">Overcomes writer's block and ideation hurdles</p>
            </div>
          </div>
          <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 text-center flex flex-col justify-between">
            <div>
              <DynamicFeed className="text-cyan-400 h-16 w-16 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">Platform Fatigue</h3>
              <p className="text-slate-400">A great blog post doesn't work as a tweet. A good Instagram caption is different. Adapting a single idea for multiple channels is repetitive and draining.</p>
            </div>
            <div className="mt-6 border-t border-slate-700/60 pt-4">
              <p className="text-3xl font-extrabold text-cyan-400">Omnichannel</p>
              <p className="text-slate-400 text-sm mt-1">Tailors one core concept across social platforms</p>
            </div>
          </div>
        </div>
      </section>

      <div className="text-center" aria-hidden="true">
        <ArrowDownward className="text-violet-500 h-20 w-20 motion-safe:animate-bounce" />
      </div>

      {/* --- Section 3: The Solution --- */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">The Solution: An AI Co-Pilot</h2>
        <div className="bg-slate-800/50 p-10 rounded-xl border border-slate-700 text-center">
          <p className="text-xl text-slate-300 leading-relaxed">
            <span className="font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">Content GenerAItor</span> wasn't built to replace creators, but to <span className="font-bold text-white">empower</span> them. It acts as a tireless creative partner, handling the repetitive, time-consuming task of adapting ideas into platform-specific formats. By automating the grunt work, it frees you to focus on what matters most: <span className="font-bold text-white">your unique voice and strategy.</span>
          </p>
        </div>
      </section>

      {/* --- Section 4: Tech Stack --- */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">Built With Modern Technology</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
          <TechLogo Icon={Code} name="React" />
          <TechLogo Icon={DataObject} name="TypeScript" />
          <TechLogo Icon={FlashOn} name="Vite" />
          <TechLogo Icon={Palette} name="Tailwind CSS" />
          <TechLogo Icon={CloudQueue} name="LLM APIs" />
        </div>
      </section>

      {/* --- Section 5: The Developer --- */}
      <section className="text-center">
        <h2 className="text-4xl font-bold mb-12">Meet the Developer</h2>
        <CreatorPhoto />
        <h3 className="text-3xl font-bold mt-6">Omar Lengua</h3>
        <p className="text-violet-400 text-xl">Full-Stack Developer & AI Enthusiast</p>
        <p className="max-w-2xl mx-auto text-slate-300 mt-4 leading-relaxed">
          I'm passionate about building tools that solve real-world problems. This project is a demonstration of how we can leverage cutting-edge AI and agentic architectures to enhance human creativity and productivity.
        </p>
        <div className="mt-8">
            <a
              href="https://github.com/Omarlsant/p-XI-llm-content-generator"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 px-8 rounded-lg shadow-lg hover:shadow-cyan-500/20 hover:-translate-y-0.5 transition-all"
            >
              View on GitHub
            </a>
        </div>
      </section>

    </div>
  );
};

export default About;
