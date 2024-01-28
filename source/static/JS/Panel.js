const add = document.getElementById('newCharacter')
const Form = document.getElementById('FormCharacter')
const Section = document.getElementById('sectionCharacters')
const exit = document.getElementById('cancel')
const inputRange = document.getElementById('range')
const spanRange = document.getElementById('rangeSpan')

add.addEventListener('click', () => {
    Section.style.display = 'none'
    Form.style.display = 'flex'
})

exit.addEventListener('click', () => {
    Form.style.display = 'none'
    Section.style.display = 'flex'
})

inputRange.addEventListener('input', () => {
    spanRange.textContent = 'Edad: ' + inputRange.value;
})

