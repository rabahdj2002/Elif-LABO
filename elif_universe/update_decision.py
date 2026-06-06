import os

content = r"""{% extends "discovery/rooms/room_base.html" %}

{% block room_projection %}
<div class="space-y-6 lg:space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700 h-full flex flex-col items-center">
    <header class="flex flex-col items-center mb-2">
        <div class="flex items-center space-x-3 mb-2">
            <div class="h-[1px] w-8 bg-gradient-to-r from-transparent to-blue-500/50"></div>
            <h2 class="text-xl lg:text-2xl font-black text-white uppercase tracking-[-0.05em]">Decision Room</h2>
            <div class="h-[1px] w-8 bg-gradient-to-l from-transparent to-blue-500/50"></div>
        </div>
        <p class="text-[9px] lg:text-[11px] text-gray-500 font-medium tracking-wide">PHASE 07: OPERATIVE TRUTH & REALITY BRANCHING</p>
    </header>

    <div class="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 flex-1 min-h-0">
        <!-- Centerpiece: The Operative Truth -->
        <div class="lg:col-span-12 flex flex-col items-center justify-center">
            <div class="w-full max-w-2xl glass-card p-10 flex flex-col items-center text-center relative overflow-hidden group shadow-[0_0_100px_rgba(59,130,246,0.05)]">
                <div class="absolute -inset-20 bg-blue-500/[0.02] blur-[100px] rounded-full group-hover:bg-blue-500/[0.05] transition-colors duration-1000"></div>
                
                <div class="relative z-10 space-y-6">
                    <div class="flex flex-col items-center">
                        <span class="text-[8px] md:text-[9px] uppercase tracking-[0.6em] text-blue-500 font-black mb-2">THE OPERATIVE TRUTH</span>
                        <h2 class="text-3xl md:text-5xl font-black text-white tracking-tighter uppercase">{{ room_data.decision|default:"Awaiting Synthesis" }}</h2>
                    </div>

                    <div class="bg-black/20 rounded-[2.5rem] p-8 border border-white/5 relative overflow-hidden">
                        <i class="fa-solid fa-quote-left text-blue-500/10 text-5xl absolute top-4 left-6"></i>
                        <p class="text-gray-300 text-base md:text-lg font-light leading-relaxed italic text-balance relative z-10">
                            "{{ room_data.summary|default:'The engine has not yet synthesized a final verdict for this inquiry.' }}"
                        </p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
                        {% for req in room_data.requirements %}
                        <div class="flex items-center space-x-3 p-4 rounded-2xl bg-blue-500/5 border border-blue-500/10 hover:bg-blue-500/10 transition-all text-left group/req">
                            <div class="w-2 h-2 rounded-full bg-blue-500/40 group-hover/req:bg-blue-400 group-hover/req:scale-125 transition-all shadow-[0_0_8px_rgba(59,130,246,0.3)]"></div>
                            <span class="text-[11px] text-gray-400 font-medium leading-snug">{{ req }}</span>
                        </div>
                        {% empty %}
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <!-- Section: Divergence Detection -->
        <div class="lg:col-span-12 space-y-6">
            <div class="flex flex-col md:flex-row items-center justify-between border-b border-white/5 pb-4 space-y-2 md:space-y-0">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                        <i class="fa-solid fa-code-branch text-[10px] text-blue-400"></i>
                    </div>
                    <h5 class="text-[10px] uppercase tracking-[0.4em] text-white/60 font-black">Navigable Trajectories</h5>
                </div>
                <span class="text-[9px] text-blue-500/60 font-mono tracking-widest uppercase">Select path to evolve substrate</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {% for divergence in room_data.divergences %}
                <div class="glass-card p-8 flex flex-col group relative overflow-hidden hover:border-blue-500/30 transition-all group/card">
                    <div class="absolute top-0 right-0 p-4 opacity-5 group-hover/card:opacity-10 transition-opacity">
                        <i class="fa-solid fa-shuffle text-3xl text-blue-400"></i>
                    </div>

                    <div class="flex justify-between items-center mb-6">
                        <span class="text-[8px] font-black text-blue-500/80 uppercase tracking-[0.3em] font-mono">DIV-{{ forloop.counter|stringformat:"02d" }}</span>
                        <div class="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-[7px] text-blue-400 font-black uppercase tracking-widest">ALTERNATIVE</div>
                    </div>

                    <h6 class="text-sm font-bold text-white mb-4 leading-tight group-hover/card:text-blue-200 transition-colors uppercase tracking-tight">
                        {{ divergence.title }}
                    </h6>

                    <p class="text-[12px] text-gray-400 leading-relaxed italic mb-8 flex-1">
                        "{{ divergence.description }}"
                    </p>

                    <form hx-post="{% url 'discovery:spawn_branch' inquiry.id %}" 
                          hx-indicator="#global-sync-overlay"
                          class="mt-auto">
                        {% csrf_token %}
                        <input type="hidden" name="title" value="{{ divergence.title }}">
                        <input type="hidden" name="description" value="{{ divergence.description }}">
                        <button type="submit" class="w-full py-4 rounded-2xl bg-blue-600/10 hover:bg-blue-600 text-blue-400 hover:text-white text-[9px] font-black uppercase tracking-[0.3em] border border-blue-500/20 transition-all flex items-center justify-center space-x-3 group/btn">
                            <span>Initialize Alternative Reality</span>
                            <i class="fa-solid fa-arrow-right text-[10px] group-hover/btn:translate-x-1 transition-transform"></i>
                        </button>
                    </form>
                </div>
                {% empty %}
                <div class="col-span-full h-40 flex flex-col items-center justify-center bg-black/20 rounded-[2rem] border border-dashed border-white/5 opacity-20">
                    <i class="fa-solid fa-link-slash text-2xl mb-4"></i>
                    <p class="text-[10px] uppercase tracking-widest">No unresolved divergences detected in this topology.</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

with open(r"c:\Users\Rabah\Desktop\ELIF V1\Elif-LABO\elif_universe\templates\discovery\rooms\decision.html", "w", encoding="utf-8") as f:
    f.write(content)
