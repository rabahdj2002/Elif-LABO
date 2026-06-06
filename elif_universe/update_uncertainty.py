import os

content = r"""{% extends "discovery/rooms/room_base.html" %}

{% block room_projection %}
<div class="space-y-6 lg:space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700 h-full flex flex-col">
    <header class="flex flex-col items-center mb-2">
        <div class="flex items-center space-x-3 mb-2">
            <div class="h-[1px] w-8 bg-gradient-to-r from-transparent to-red-500/50"></div>
            <h2 class="text-xl lg:text-2xl font-black text-white uppercase tracking-[-0.05em]">Uncertainty Room</h2>
            <div class="h-[1px] w-8 bg-gradient-to-l from-transparent to-red-500/50"></div>
        </div>
        <p class="text-[9px] lg:text-[11px] text-gray-500 font-medium tracking-wide">PHASE 06: RESIDUAL DARKNESS & LOAD-BEARING GAPS</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 flex-1 min-h-0">
        <!-- Main Panel: Residual Darkness -->
        <div class="lg:col-span-12 flex flex-col min-h-0">
            <div class="glass-card p-8 flex flex-col flex-1 min-h-0 relative overflow-hidden group border-red-500/10 shadow-[0_0_50px_rgba(239,68,68,0.05)]">
                <div class="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                    <i class="fa-solid fa-moon text-5xl text-red-400"></i>
                </div>

                <div class="flex items-center space-x-3 mb-8">
                    <div class="w-10 h-10 rounded-xl bg-red-500/10 flex items-center justify-center border border-red-500/20">
                        <i class="fa-solid fa-cloud-moon text-xs text-red-500"></i>
                    </div>
                    <div>
                        <h4 class="text-[10px] uppercase tracking-[0.3em] text-red-500 font-black">Residual Darkness</h4>
                        <p class="text-[8px] text-gray-500 font-mono tracking-widest">UNRESOLVED SEMANTIC ZONES</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 flex-1 min-h-0">
                    {% if inquiry.unresolved_zones %}
                        {% for zone in inquiry.unresolved_zones %}
                        <div class="p-6 rounded-[2rem] bg-black/40 border border-white/5 flex flex-col justify-center hover:border-red-500/30 transition-all group/zone relative overflow-hidden">
                            <div class="absolute -left-10 -top-10 w-24 h-24 bg-red-500/[0.02] blur-[40px] rounded-full"></div>
                            <div class="relative z-10 flex items-start space-x-4">
                                <div class="w-1.5 h-1.5 rounded-full bg-red-500/40 mt-1.5 animate-pulse shrink-0"></div>
                                <p class="text-[12px] text-gray-300 leading-relaxed italic font-medium">"{{ zone }}"</p>
                            </div>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="col-span-3 h-full flex flex-col items-center justify-center opacity-30 text-center py-20 bg-black/40 rounded-[2rem] border border-dashed border-white/5">
                            <i class="fa-solid fa-certificate text-3xl mb-4 text-green-500/40"></i>
                            <p class="text-[10px] uppercase tracking-[0.4em] font-black">Semantic convergence achieved</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Sub Panels: Biases & Ambiguities -->
        <div class="lg:col-span-6 flex flex-col min-h-0 space-y-6">
            <div class="glass-card p-6 flex flex-col h-full min-h-0 group relative overflow-hidden">
                <div class="flex items-center space-x-3 mb-6">
                    <div class="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center border border-white/10">
                        <i class="fa-solid fa-microchip text-[10px] text-gray-500"></i>
                    </div>
                    <h4 class="text-[10px] uppercase tracking-[0.3em] text-gray-500 font-black">Falsification Conditions</h4>
                </div>

                <div class="flex-1 overflow-y-auto custom-scrollbar pr-2 space-y-3">
                    {% for bias in room_data.biases %}
                    <div class="p-4 rounded-xl bg-white/[0.01] border border-white/5 group/bias hover:border-red-500/20 transition-all">
                        <div class="text-[8px] font-mono text-gray-600 uppercase tracking-widest mb-2 group-hover/bias:text-red-500/60">{{ bias.name }}</div>
                        <p class="text-[11px] text-gray-400 leading-tight italic">"Potential failure if: {{ bias.impact }}"</p>
                    </div>
                    {% empty %}
                    <div class="h-full flex items-center justify-center text-[10px] text-gray-600 italic">No structural failure routes identified.</div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <div class="lg:col-span-6 flex flex-col min-h-0 space-y-6">
            <div class="glass-card p-6 flex flex-col h-full min-h-0 group relative overflow-hidden">
                <div class="flex items-center space-x-3 mb-6">
                    <div class="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center border border-white/10">
                        <i class="fa-solid fa-fingerprint text-[10px] text-gray-500"></i>
                    </div>
                    <h4 class="text-[10px] uppercase tracking-[0.3em] text-gray-500 font-black">Unresolved Ambiguities</h4>
                </div>

                <div class="flex-1 overflow-y-auto custom-scrollbar pr-2 space-y-3">
                    {% for entry in room_data.ambiguities %}
                    <div class="flex items-start space-x-4 p-4 rounded-xl bg-white/[0.01] border border-white/5 hover:bg-white/[0.04] transition-all">
                        <div class="w-8 h-8 rounded-lg bg-black/40 border border-white/5 flex items-center justify-center text-gray-600 text-[10px] shrink-0">
                            {% if entry.kind == 'capacity_change' %}<i class="fa-solid fa-battery-half"></i>
                            {% elif entry.kind == 'pattern_engaged' %}<i class="fa-solid fa-dna"></i>
                            {% elif entry.kind == 'judgment_act' %}<i class="fa-solid fa-gavel text-red-500/40"></i>
                            {% else %}<i class="fa-solid fa-circle-question"></i>{% endif %}
                        </div>
                        <div>
                            <div class="text-[8px] text-gray-600 uppercase font-black tracking-widest mb-1">{{ entry.kind }}</div>
                            <p class="text-[11px] text-gray-400 leading-tight font-medium">{{ entry.description }}</p>
                        </div>
                    </div>
                    {% empty %}
                    <div class="h-full flex items-center justify-center text-[10px] text-gray-600 italic">No residual ambiguities detected.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

with open(r"c:\Users\Rabah\Desktop\ELIF V1\Elif-LABO\elif_universe\templates\discovery\rooms\uncertainty.html", "w", encoding="utf-8") as f:
    f.write(content)
