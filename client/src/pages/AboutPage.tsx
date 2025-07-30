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
import photoImg from '../assets/photo.jpg'; // Make sure to replace with your actual photo path


// Placeholder for your photo
const YourPhoto = () => (
  <div className="w-48 h-48 bg-gradient-to-br from-cyan-500 to-violet-600 rounded-full mx-auto shadow-lg">
    <img
      src={photoImg}
      alt="Your Name"
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
        <p className="mt-4 text-2xl font-semibold text-violet-400">Our Mission and the 'Why' Behind Post GenerAItor</p>
      </section>

      {/* --- Section 2: The Problem --- */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">The Creator's Dilemma</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 text-center">
            <HourglassEmpty className="text-cyan-400 h-16 w-16 mx-auto mb-4" />
            <h3 className="text-2xl font-bold mb-2">The Time Sink</h3>
            <p className="text-slate-400">Brainstorming, drafting, and tailoring content for different platforms can consume an entire day's work. Quality content demands significant time investment.</p>
            <p className="text-5xl font-extrabold text-cyan-400 mt-6">8+</p>
            <p className="text-slate-500 font-semibold">Hours per week on average</p>
          </div>
          <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 text-center">
            <LightbulbOutlined className="text-cyan-400 h-16 w-16 mx-auto mb-4" />
            <h3 className="text-2xl font-bold mb-2">Creative Burnout</h3>
            <p className="text-slate-400">The constant pressure to be original and engaging leads to writer's block. Inspiration is a finite resource that needs to be managed carefully.</p>
            <p className="text-5xl font-extrabold text-cyan-400 mt-6">72%</p>
            <p className="text-slate-500 font-semibold">of creators report burnout</p>
          </div>
          <div className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 text-center">
            <DynamicFeed className="text-cyan-400 h-16 w-16 mx-auto mb-4" />
            <h3 className="text-2xl font-bold mb-2">Platform Fatigue</h3>
            <p className="text-slate-400">A great blog post doesn't work as a tweet. A good Instagram caption is different. Adapting a single idea for multiple channels is repetitive and draining.</p>
            <p className="text-5xl font-extrabold text-cyan-400 mt-6">3x</p>
            <p className="text-slate-500 font-semibold">the effort for 3 platforms</p>
          </div>
        </div>
      </section>

      <div className="text-center">
        <ArrowDownward className="text-violet-500 h-20 w-20 animate-bounce" />
      </div>

      {/* --- Section 3: The Solution --- */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">The Solution: An AI Co-Pilot</h2>
        <div className="bg-slate-800/50 p-10 rounded-xl border border-slate-700 text-center">
          <p className="text-xl text-slate-300 leading-relaxed">
            <span className="font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">Post GenerAItor</span> wasn't built to replace creators, but to <span className="font-bold text-white">empower</span> them. It acts as a tireless creative partner, handling the repetitive, time-consuming task of adapting ideas into platform-specific formats. By automating the grunt work, it frees you to focus on what matters most: <span className="font-bold text-white">your unique voice and strategy.</span>
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
        <YourPhoto />
        <h3 className="text-3xl font-bold mt-6">Omar Lengua</h3>
        <p className="text-violet-400 text-xl">Full-Stack Developer & AI Enthusiast</p>
        <p className="max-w-2xl mx-auto text-slate-300 mt-4">
          I'm passionate about building tools that solve real-world problems. This project is a demonstration of how we can leverage cutting-edge AI to enhance human creativity and productivity.
        </p>
        <div className="mt-8">
            <a href="https://github.com/your-username" target="_blank" rel="noopener noreferrer" className="inline-block bg-slate-700 text-white font-semibold py-3 px-8 rounded-lg shadow-lg hover:bg-slate-600 transition-colors">
              View on GitHub
            </a>
        </div>
      </section>

    </div>
  );
};

export default About;