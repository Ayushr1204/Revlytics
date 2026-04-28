TOPICS = {
    "laptops": ["battery","performance","heat","noise","build"],
    "smartphones": ["battery","camera","performance","heat","display"],
    "headphones": ["audio","comfort","battery","anc","build"],
    "monitors": ["display","brightness","refresh","color","build"],
}

CHUNK_TOPIC_MAP = {
    "battery":"battery","performance":"performance","heat":"heat","noise":"noise",
    "build":"build","camera":"camera","display":"display","audio":"audio",
    "comfort":"general","anc":"audio","brightness":"display","refresh":"display","color":"display",
}

RANGES = {
    "battery_pos":(7.0,10.5),"battery_neu":(4.5,7.0),"battery_neg":(2.5,4.5),
    "temp_pos":(35,41),"temp_neu":(42,48),"temp_neg":(49,57),
    "noise_pos":(28,35),"noise_neu":(36,44),"noise_neg":(45,55),
    "fps_pos":(100,165),"fps_neu":(60,99),"fps_neg":(30,59),
    "lag_pos":(15,40),"lag_neu":(50,180),"lag_neg":(200,400),
    "bright_pos":(450,600),"bright_neu":(300,449),"bright_neg":(200,299),
    "refresh_pos":(144,360),"refresh_neu":(75,143),"refresh_neg":(60,74),
    "cpu_pos":(30,55),"cpu_neu":(56,80),"cpu_neg":(81,99),
}

# Templates: {n}=product name, {v}=value, {v2}=secondary value
# Format: list of (template_string, topic_for_chunk)
T = {
"laptops": {
"battery": {
"pos":[
"{n} easily lasts {v} hours during my usual mix of coding and browsing",
"I can skip the charger because the {n} holds about {v} hours through office apps and Wi-Fi",
"Battery life on the {n} fits its portable design well, lasting {v} hours in my mixed workday",
"The {n} comfortably runs {v} hours between charges during light development work",
"With screen brightness at fifty percent, the {n} pushes past {v} hours on a workday",
"On a cross-country flight, the {n} held steady for {v} hours of writing and spreadsheets",
],
"neu":[
"Battery hours on the {n} sit around {v} hours when brightness stays at medium",
"The {n} manages about {v} hours on battery, which covers most of my morning meetings",
"Battery on the {n} is neither great nor terrible, landing around {v} hours in practice",
"With moderate use the {n} gives roughly {v} hours, enough if you plan around it",
"The {n} delivers {v} hours of battery, adequate for a half-day away from the desk",
],
"neg":[
"Battery drain on the {n} is rough, with only {v} hours when VS Code and Chrome stay open",
"During travel, the {n} loses charge so quickly that {v} hours is the realistic ceiling",
"The {n} barely survives {v} hours on battery, which is frustrating for any mobile workflow",
"I expected more from the {n} but battery tops out at {v} hours with light multitasking",
"With Wi-Fi on, the {n} dies in {v} hours, forcing me to carry the charger everywhere",
],
},
"performance": {
"pos":[
"The {n} keeps frame pacing stable around {v} FPS during my usual evening games",
"In shooter matches, the {n} stays near {v} FPS without the stutter I expected from a laptop",
"During Rails work in a coffee shop, the {n} keeps CPU usage around {v2}% and cursor lag stays below {v} ms",
"Compiling large projects on the {n} finishes fast with CPU headroom to spare",
"The {n} handles Docker containers alongside VS Code without breaking a sweat",
],
"neu":[
"Frame rates on the {n} hover near {v} FPS, which is playable but not exciting",
"The {n} starts around {v} FPS in games, then dips after the fans settle into a louder curve",
"During Python scripts between meetings, the {n} reaches {v2}% CPU and shows brief lag when I switch apps",
"With my quiet office workflow, the {n} pauses for {v} ms when Docker logs and browser tabs update together",
"The {n} can handle everyday tasks but starts showing its limits with heavier workloads",
],
"neg":[
"With backend services open, the {n} keeps CPU usage near {v2}% long enough to slow window switching",
"For heavier coding, the {n} drops into {v} ms of lag whenever tests and Chrome run together",
"The {n} cannot hold stable FPS in modern games, sliding from {v} FPS to {v2} FPS within minutes",
"Multitasking on the {n} is painful because everything stutters after ten browser tabs",
"The {n} chokes on compilation tasks that my older desktop handled without issue",
],
},
"heat": {
"pos":[
"Heat management suits the {n} well because palm-rest temperature stays under {v} C",
"Thermals are controlled on the {n}, with the keyboard deck staying near {v} C after a long build",
"The {n} stays surprisingly cool at {v} C even during extended coding sessions",
"Surface temperatures on the {n} remain comfortable at {v} C during normal office work",
],
"neu":[
"Temperature on the {n} climbs to {v} C during video calls, mostly around the exhaust area",
"The {n} gets warm at {v} C near the hinge during VS Code sessions, though it cools after a few minutes idle",
"In my home setup, the {n} hits {v} C after compile loops but stays usable",
"The {n} warms up to {v} C under sustained load, which is about what I expected at this price",
],
"neg":[
"The {n}'s thermal behavior is poor because the palm-rest area warms to {v} C under normal coding load",
"Temperature spikes on the {n} hit {v} C after fifteen minutes of gaming",
"The {n} gets uncomfortably hot at {v} C during video rendering, making lap use impossible",
"Bottom panel of the {n} reaches {v} C regularly, and I worry about long-term component health",
],
},
"noise": {
"pos":[
"Fan noise on the {n} stays around {v} dB during office work, so calls remain clear",
"The {n} runs nearly silent at {v} dB under normal workloads, which I appreciate in quiet rooms",
"Even during moderate compilation, the {n} keeps fan noise down to {v} dB",
"The {n} whispers along at {v} dB during browsing and document editing",
],
"neu":[
"Fan noise on the {n} rises to {v} dB during test runs, which is noticeable but not constant",
"The {n} gets loud at {v} dB when CPU usage stays high for more than ten minutes",
"Acoustics on the {n} sit around {v} dB under load, tolerable with music playing",
"The {n} fan ramps to {v} dB during builds, enough to notice but not enough to disrupt calls",
],
"neg":[
"The {n} produces a sharp fan tone at {v} dB, which makes quiet-room coding unpleasant",
"The {n} fan hits about {v} dB during builds, and the pitch cuts through meetings",
"Fan noise on the {n} is unbearable at {v} dB, drowning out my music easily",
"Working late at night, the {n} fan at {v} dB wakes everyone in the room",
],
},
"build": {
"pos":[
"Build quality on the {n} feels firm, with no lid creak when I carry it between desks",
"The keyboard deck on the {n} has minimal flex, so long coding sessions feel precise",
"The {n} feels solid in hand with tight tolerances and a premium hinge mechanism",
"Chassis rigidity on the {n} inspires confidence when tossing it into a backpack",
],
"neu":[
"Build quality on the {n} is acceptable, although the lid flexes slightly when opened from one corner",
"The hinge on the {n} is stable enough for office use, yet it wobbles when I tap the touchscreen",
"The {n} feels decent for its price, though the plastic bottom panel cheapens the look",
"Materials on the {n} are fine overall, nothing that stands out positively or negatively",
],
"neg":[
"The {n}'s hinge creaks after a week of use, making the laptop feel cheaper than expected",
"Build quality on the {n} disappoints because the keyboard deck flexes noticeably during typing",
"The {n} creaks whenever I adjust the screen angle, which does not inspire confidence",
"After two months, the {n} shows visible wear on the palm rest and the trackpad wobbles",
],
},
},
"smartphones": {
"battery": {
"pos":[
"The {n} easily lasts a full workday with {v} hours of screen-on time",
"Battery on the {n} is outstanding, giving me {v} hours of mixed use without worry",
"I get through an entire day on the {n} with {v} hours of active screen time to spare",
"Even with heavy social media scrolling, the {n} holds {v} hours of screen time",
"The {n} charges from empty to full in under an hour, and the {v}-hour battery life is solid",
],
"neu":[
"Screen-on time on the {n} lands around {v} hours, enough to get through most of the day",
"The {n} lasts about {v} hours with moderate use, so I charge it every evening",
"Battery performance on the {n} is average at {v} hours, nothing remarkable",
"The {n} delivers {v} hours, which is acceptable but I keep a charger at work just in case",
],
"neg":[
"Battery on the {n} barely hits {v} hours with normal scrolling and messaging",
"The {n} drains faster than expected, giving only {v} hours of real screen-on time",
"I have to charge the {n} twice a day because {v} hours of screen time is all it can manage",
"Battery life on the {n} is disappointing at {v} hours, especially at this price point",
],
},
"camera": {
"pos":[
"Photos from the {n} look sharp in daylight with natural colors and good dynamic range",
"The {n} captures excellent night shots without excessive grain or noise",
"Portrait mode on the {n} nails the edge detection and produces bokeh that looks natural",
"Video stabilization on the {n} is impressive even while walking on uneven sidewalks",
"The {n} camera handles tricky backlit scenes better than any phone I have used before",
],
"neu":[
"Camera on the {n} is solid in good light but struggles a bit when indoors",
"The {n} takes decent photos for social media, though dedicated camera phones do better",
"Daytime shots on the {n} are sharp, but low-light images get noticeably grainy",
"The {n} camera is fine for everyday snapshots but lacks the punch for serious photography",
],
"neg":[
"Night photography on the {n} is poor, with heavy noise and washed-out colors",
"The {n} camera overprocesses skin tones, making portraits look artificial",
"Autofocus on the {n} hunts constantly in low light, ruining many shots",
"Video recorded on the {n} shows visible jitter that software stabilization cannot fix",
],
},
"performance": {
"pos":[
"The {n} runs smoothly even with multiple apps open and no noticeable stutter",
"Gaming on the {n} is surprisingly fluid, holding steady frame rates in most titles",
"App switching on the {n} is instant, and heavy apps like Lightroom load in seconds",
"The {n} handles multitasking without hesitation, keeping a dozen apps in memory",
],
"neu":[
"Performance on the {n} is fine for daily use but heavier games show occasional frame drops",
"The {n} handles routine tasks well enough, though it pauses briefly with many apps open",
"Day-to-day speed on the {n} is acceptable, nothing that frustrates or impresses",
"The {n} gets the job done for social media and messaging without major complaints",
],
"neg":[
"The {n} starts lagging after prolonged use, especially with social media apps",
"Apps on the {n} take noticeably long to open and switching between them feels sluggish",
"The {n} stutters during basic multitasking, which is unacceptable at this price",
"Gaming on the {n} is a bad experience with constant frame drops and touch input delays",
],
},
"heat": {
"pos":[
"The {n} stays cool even during long video calls and streaming sessions",
"Thermal management on the {n} is excellent, barely warming up during gaming",
"Even after thirty minutes of navigation in the sun, the {n} remains comfortable to hold",
"The {n} dissipates heat efficiently, never getting hot enough to be uncomfortable",
],
"neu":[
"The {n} gets warm during extended gaming but cools down quickly once I stop",
"Heating on the {n} is noticeable during video calls but not uncomfortable",
"The {n} warms up around the camera module during heavy use, which seems normal",
"Temperature on the {n} is manageable, though I notice warmth near the top after streaming",
],
"neg":[
"The {n} gets uncomfortably hot during gaming sessions, almost too warm to hold",
"Heating on the {n} is a real issue during video recording, forcing me to take breaks",
"The {n} overheats during extended camera use and throttles performance noticeably",
"After twenty minutes of gaming, the {n} feels like a hand warmer and starts to lag",
],
},
"display": {
"pos":[
"The {n} display is vibrant with punchy colors and excellent outdoor visibility",
"Screen on the {n} looks gorgeous, with deep blacks and smooth scrolling at 120 Hz",
"The {n} display gets bright enough for direct sunlight without washing out",
"Watching content on the {n} is a pleasure thanks to its sharp and color-accurate panel",
],
"neu":[
"Display on the {n} is decent for the price, with acceptable color reproduction",
"The {n} screen handles everyday content fine, though it could be brighter outdoors",
"Colors on the {n} display are a bit muted compared to flagships but perfectly usable",
"The {n} has a serviceable display that does not disappoint but does not wow either",
],
"neg":[
"The {n} display washes out badly in sunlight, making outdoor use frustrating",
"Screen quality on the {n} is below average with dull colors and poor viewing angles",
"The {n} display flickers at low brightness, which causes eye strain during night reading",
"Blacks on the {n} screen look more like dark grey, ruining the experience for dark content",
],
},
},
"headphones": {
"audio": {
"pos":[
"Sound quality on the {n} is exceptional with clear highs and punchy bass",
"The {n} delivers a wide soundstage that makes music feel immersive and layered",
"Bass on the {n} hits deep without muddying the mids, perfect for electronic and hip-hop",
"Instrument separation on the {n} is impressive, letting me pick out individual tracks easily",
"The {n} reproduces vocals with stunning clarity that reveals details I missed before",
],
"neu":[
"Audio on the {n} is decent for the price, with balanced sound across most genres",
"The {n} sounds fine for casual listening, though audiophiles might want more detail",
"Bass on the {n} is present but not overwhelming, which suits podcast listening well",
"Sound profile on the {n} is fairly flat, good for mixing but less exciting for casual music",
],
"neg":[
"The {n} sounds tinny at higher volumes, with harsh treble that causes fatigue",
"Bass on the {n} is almost nonexistent, making bass-heavy genres sound hollow",
"Audio quality on the {n} distorts noticeably above seventy percent volume",
"The {n} has a narrow soundstage that makes everything feel compressed and flat",
],
},
"comfort": {
"pos":[
"The {n} feels weightless during long listening sessions, even after four hours straight",
"Ear cushions on the {n} are plush and breathable, perfect for all-day office wear",
"I forget I am wearing the {n} because the clamping pressure is perfectly balanced",
"The {n} fits comfortably over glasses without creating pressure points on my temples",
],
"neu":[
"Comfort on the {n} is acceptable for sessions up to two hours before I need a break",
"The {n} fits well enough, though the ear cups could be a bit deeper for larger ears",
"Wearing the {n} is fine for commuting, but extended studio sessions make my ears warm",
"The headband on the {n} is padded enough, though it leaves a dent after long use",
],
"neg":[
"The {n} clamps too tightly, causing headaches after an hour of continuous use",
"Ear pads on the {n} trap heat badly, making summer listening sessions miserable",
"The {n} is uncomfortable for glasses wearers because the pads press hard on the frames",
"After thirty minutes, the {n} starts hurting the top of my head due to poor padding",
],
},
"battery": {
"pos":[
"Battery on the {n} is stellar, lasting {v} hours of continuous playback",
"The {n} runs for {v} hours on a single charge, easily covering my entire work week of commutes",
"I charge the {n} once a week with {v} hours of battery life and daily two-hour sessions",
"The {n} holds {v} hours of juice with ANC on, which is more than enough for long flights",
],
"neu":[
"Battery life on the {n} sits around {v} hours, which is average for this class",
"The {n} manages {v} hours of playback, enough for daily commutes but not marathon sessions",
"With ANC enabled, the {n} gives about {v} hours before needing a top-up",
"Battery on the {n} is nothing special at {v} hours, but the quick charge helps",
],
"neg":[
"The {n} only lasts {v} hours on a charge, which barely covers a transatlantic flight",
"Battery on the {n} drains to {v} hours with ANC on, far short of the advertised number",
"I have to charge the {n} almost daily because {v} hours does not last through my commutes",
"The {n} dies at {v} hours, frustrating when I am mid-podcast on a long train ride",
],
},
"anc": {
"pos":[
"Noise cancellation on the {n} blocks out office chatter and keyboard clatter completely",
"ANC on the {n} silences airplane engine drone so well I can hear whispered dialogue in movies",
"The {n} cancels low-frequency hum impressively, making my commute peaceful",
"Switching on ANC on the {n} feels like stepping into a soundproof room",
],
"neu":[
"ANC on the {n} handles steady noise like fans but lets sharper sounds through",
"Noise cancellation on the {n} is decent for an office environment but not perfect on flights",
"The {n} reduces background noise noticeably, though voices still bleed through at times",
"ANC performance on the {n} is middle of the road, fine for commuting but not isolation-level",
],
"neg":[
"Noise cancellation on the {n} is weak, barely reducing the hum of an air conditioner",
"ANC on the {n} introduces a noticeable hiss that is distracting during quiet music",
"The {n} does almost nothing to block human speech, defeating the purpose of ANC",
"Wind noise renders the {n} ANC useless outdoors, which limits its usefulness",
],
},
"build": {
"pos":[
"The {n} feels premium with solid hinges and a satisfying fold mechanism",
"Build quality on the {n} is excellent, surviving daily tossing into bags without issue",
"Materials on the {n} feel high-end with smooth plastic and sturdy metal accents",
"The {n} folds flat and feels durable enough to last years of daily commuting",
],
"neu":[
"Build on the {n} is adequate, though the plastic creaks slightly when adjusting fit",
"The {n} feels decent in hand but the headband adjustment clicks are a bit loose",
"Construction of the {n} is fine for the price, nothing fragile but nothing luxurious",
"The {n} is built well enough for indoor use but I would not trust it for gym workouts",
],
"neg":[
"The {n} feels flimsy with thin plastic arms that I worry will snap over time",
"Build quality on the {n} is disappointing with visible seam gaps and cheap hinges",
"The {n} headband cracked at the adjustment slider after three months of normal use",
"Materials on the {n} feel cheap and the ear cup swivel loosened within weeks",
],
},
},
"monitors": {
"display": {
"pos":[
"The {n} delivers stunning image quality with razor-sharp text and vivid colors",
"Picture clarity on the {n} is outstanding, making photo editing a genuine pleasure",
"The {n} panel produces deep blacks and wide viewing angles that impress from any seat",
"Every pixel on the {n} feels purposeful, text rendering is crisp even at small font sizes",
],
"neu":[
"Display quality on the {n} is fine for office work and casual media consumption",
"The {n} shows clear images but does not stand out against pricier panels",
"Image quality on the {n} meets expectations for the segment without exceeding them",
"The {n} panel handles most content well, though dark scenes reveal some banding",
],
"neg":[
"The {n} suffers from noticeable backlight bleed in the corners during dark scenes",
"Text on the {n} looks slightly fuzzy at native resolution, which bothers me during coding",
"The {n} panel has uneven brightness that becomes obvious on solid-color backgrounds",
"Image quality on the {n} is underwhelming with washed-out colors straight from the box",
],
},
"brightness": {
"pos":[
"The {n} peaks at {v} nits, easily visible even with afternoon sun hitting the screen",
"Brightness on the {n} reaches {v} nits, making HDR content pop beautifully",
"At {v} nits the {n} handles my sunlit home office without any glare issues",
"The {n} gets bright enough at {v} nits that I never squint during daytime use",
],
"neu":[
"Brightness on the {n} sits around {v} nits, which works indoors but struggles in sunlight",
"The {n} reaches {v} nits, adequate for a room with curtains but not great near windows",
"At {v} nits the {n} is average for its class, fine for most controlled environments",
"The {n} provides {v} nits of brightness, serviceable but I wish it went higher",
],
"neg":[
"The {n} maxes out at {v} nits, making it nearly unusable in my bright living room",
"Brightness on the {n} tops at {v} nits, and HDR content looks dull as a result",
"At only {v} nits the {n} forces me to draw the blinds just to see the screen properly",
"The {n} is far too dim at {v} nits for any room with natural light",
],
},
"refresh": {
"pos":[
"The {n} at {v} Hz makes scrolling buttery smooth and cursor movement precise",
"Gaming on the {n} at {v} Hz feels incredibly responsive with no visible tearing",
"At {v} Hz the {n} transforms everyday desktop use into a noticeably fluid experience",
"The {n} refresh rate of {v} Hz eliminates motion blur in fast-paced shooter games",
],
"neu":[
"The {n} runs at {v} Hz, which is smooth enough for general use and light gaming",
"At {v} Hz the {n} handles office work and video fine, though competitive gamers may want more",
"Refresh rate on the {n} at {v} Hz is acceptable, a step up from sixty but not top tier",
"The {n} delivers {v} Hz, adequate for my casual gaming but I notice the difference from faster panels",
],
"neg":[
"At {v} Hz the {n} feels sluggish compared to higher-refresh monitors I have used",
"The {n} is limited to {v} Hz, which introduces visible motion blur in fast games",
"Scrolling on the {n} at {v} Hz feels choppy, especially after using a faster display",
"The {n} at {v} Hz makes desktop animations feel dated and cursor tracking imprecise",
],
},
"color": {
"pos":[
"Color accuracy on the {n} is exceptional, matching my calibrated prints almost perfectly",
"The {n} covers a wide gamut with Delta E values low enough for professional color grading",
"Out of the box, the {n} displays accurate and balanced colors without any calibration",
"The {n} reproduces skin tones naturally, which makes portrait editing reliable",
],
"neu":[
"Colors on the {n} are decent after calibration, though the factory profile skews warm",
"The {n} handles sRGB content well but falls short on wider color spaces",
"Color reproduction on the {n} is average, fine for office documents but not for print work",
"The {n} shows acceptable colors for everyday use, though reds lean slightly orange",
],
"neg":[
"Color accuracy on the {n} is poor out of the box, with an obvious blue tint everywhere",
"The {n} struggles with color consistency across the panel, visible on gradient test patterns",
"Reds on the {n} look oversaturated and greens shift toward yellow in a distracting way",
"Calibrating the {n} only partially fixes the color issues, and it drifts back within weeks",
],
},
"build": {
"pos":[
"The {n} stand is sturdy with smooth height and tilt adjustments that stay put",
"Build quality on the {n} feels premium with thin bezels and a solid metal base",
"The {n} has excellent cable management with a channel built into the stand",
"Assembly of the {n} is tool-free and the whole unit feels rock solid on my desk",
],
"neu":[
"The {n} stand is functional but only offers tilt adjustment, no height or swivel",
"Build on the {n} is average with plastic construction that does the job",
"The {n} wobbles slightly when I bump the desk, though it is not a major concern",
"Construction of the {n} is acceptable, bezels are a bit thick but the stand works fine",
],
"neg":[
"The {n} stand is wobbly and the monitor shakes every time I type on the desk",
"Build quality on the {n} feels cheap with flimsy plastic and thick bezels",
"The {n} stand offers no height adjustment, forcing me to stack books underneath",
"Bezels on the {n} are distractingly large and the base takes up too much desk space",
],
},
},
}
