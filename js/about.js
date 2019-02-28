var LEVEL_UP = new Date(2017, 07, 13);

var SKILL_DESCS = [
    "I really love biking! It's the only exercise I like, actually.",
     "Videogames are my passion and my hobby since I was a little kid. My first console was a SNES, followed by a PS One, an Xbox 360 and a Wii, and a Gameboy Advance SP, a Nintendo DS and a Nintendo 3DS as handheld consoles. My favorite genres are RPG (such as 'The Elder Scrolls' and 'Pokémon' series), Strategy (such as 'Civilization' and 'Age of Empires' series), Simulation (such as 'Sim City' and 'The Sims' series), Sandbox (such as 'Minecraft' and the 'Grand Theft Auto' series) and Adventure (such as the 'Assassin's Creed' and 'The Legend of Zelda' series).",
     "I really like riddles and puzzles, and any other action that involves logical thinking (such as programming and playing videogames). I tend to over-analyze situations and always try to find a logical reason to everything.",
     "My formation as a programmer has given me a great skill to solve problems. Also, since I'm doing research in Algorithmic Science, I can solve problems not only effectively, but also solve them efficiently.",
     "I found programming a really pleasurable and rewarding experience. Programming synthesizes some of the activities I like, such as logical reasoning and problem solving, and as any good programmer, I like to learn new things and take on new challenges. Every line of code matters and makes you a better programmer!",
     "Reading is an activity I enjoy since a long time ago. I learnt to read when I was 5 years old, and haven't stopping since. My favorite genres are comedies and mystery novels, but generally I enjoy any good book. My favorite books are 'The Three Musketeers' by Alexandre Dumas, 'A Study in Scarlet' by Sir Arthur Conan Doyle, 'Les Misérables' by Victor Hugo, 'Tartuffe' by Molière and 'Fahrenheit 451' by Rad Bradbury.",
     "I'm a really shy person. It's very difficult to me to have conversations with new people, which causes that I only have very few friends. But once I get to know a person a little better, I start to be a very goofy and funny person. Give me a change and you may even like me!" 
];

var SKILL_IMGS = [
    "skill01.png", "skill02.png", "skill03.png", "skill04.png",
    "skill05.png", "skill06.png", "skill07.png"
];

var SKILL_NAMES = [
    "Bike", "Gaming", "Logic", "Problem solving", "Programming",
    "Reading", "Speech"
];

function init() {
    progress = Math.floor((LEVEL_UP - new Date()) / (1000 * 60 * 60 * 24));

    console.log(progress);

    $('#next-lvl').attr('value', 366 - progress);
    $('.skill-row').click(function(){
        loadSkillInfo($(this).children('.skill-name').attr('data-skillid'));
    });
}

function loadSkillInfo(skillID) {
	console.log(skillID);
	
	$('#cur-skill-name').html(SKILL_NAMES[skillID]);
	$('#cur-skill-img').attr('src', 'img/' + SKILL_IMGS[skillID]);
	$('#cur-skill-desc').html(SKILL_DESCS[skillID]);
}
