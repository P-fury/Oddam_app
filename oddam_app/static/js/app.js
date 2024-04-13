document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);


                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });

        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {

                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");


                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
            const numberOfBags = getNumberOfBags();
            updateSummaryBags(numberOfBags);
            updateSummaryAndRetrieveOrganizationName();
            pickupFormSaveAndWrite();
            // writeFromPickupDict()
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});

/**
 * Category selector
 * Creating list of selected cagtegories.
 * Using filter function
 */
const categorycheckboxes = document.querySelectorAll('input[name="categories"]');
const selectedCategories = [];
categorycheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
        if (this.checked) {
            selectedCategories.push(this.value);

        } else {
            const index = selectedCategories.indexOf(this.value);
            if (index !== -1) {
                selectedCategories.splice(index, 1)
            }

        }
        filterInstCategories(selectedCategories)
    })
})

/**
 * For every hidden data-value if equal selected checkbox
 * Change visibility from none to block
 */
function filterInstCategories(categories) {
    const institutions = document.querySelectorAll('[data-step="3"] .form-group--checkbox');
    institutions.forEach(function (institution) {
        const categoriesInInstitution = institution.querySelectorAll('.categories_of_institutions');
        let showInstitution = false;
        categoriesInInstitution.forEach(function (category) {
            if (categories.includes(category.dataset.value)) {
                showInstitution = true;
            }
        });
        if (showInstitution) {
            institution.style.display = 'block';

        } else {
            institution.style.display = 'none';
        }
    })
}

/**
 * remember bags
 */
function getNumberOfBags() {
    const bagsInput = document.querySelector('input[name="bags"]');
    // const PostForm = document.querySelector('input[id="amount_of_bags"]');

    if (bagsInput) {
        // PostForm.value = bagsInput
        return parseInt(bagsInput.value);

    } else {
        return null;
    }
}


/**
 * update summary of bags
 */

function updateSummaryBags(numberOfBags) {
    const summaryTextElement = document.querySelector('.form-section .summary--text');
    if (summaryTextElement) {
        if (numberOfBags === 1) {
            summaryTextElement.textContent = `${numberOfBags} worek z ${selectedCategories}`;
        } else {
            summaryTextElement.textContent = `${numberOfBags} worki z ${selectedCategories}`;
        }

    }
}

/**
 * upate summary of organizaion
 */
function updateSummaryAndRetrieveOrganizationName() {
    const organizationChoice = document.querySelectorAll('input[name="organization"]');
    const summaryTextElements = document.querySelectorAll('.summary--text');
    const organizationType = document.querySelector('.type-of-organization').innerText

    organizationChoice.forEach(radio => {
        radio.addEventListener('change', function () {
            const selectedOrganizationName = this.parentElement.querySelector('.title').innerText;
            if (selectedOrganizationName) {
                summaryTextElements.forEach((element, index) => {
                    if (index === 1) {
                        element.textContent = `Dla ${organizationType} "${selectedOrganizationName}"`;
                    }
                });
            }
        });
    });
}

function pickupFormSaveAndWrite() {
    const nextButton = document.querySelector('.form--steps [data-step="4"] .next-step');
    const pickupForm = document.getElementById('pickup_form');
    let addressDict = {};
    let dateScheduleDict = {}

    nextButton.addEventListener('click', function () {
        addressDict.address = pickupForm.querySelector('input[name="address"]').value;
        addressDict.city = pickupForm.querySelector('input[name="city"]').value;
        addressDict.postcode = pickupForm.querySelector('input[name="postcode"]').value;
        addressDict.phone = pickupForm.querySelector('input[name="phone"]').value;
        dateScheduleDict.date = pickupForm.querySelector('input[name="data"]').value;
        dateScheduleDict.time = pickupForm.querySelector('input[name="time"]').value;
        dateScheduleDict.moreInfo = pickupForm.querySelector('textarea[name="more_info"]').value;
        console.log(addressDict, dateScheduleDict)
        writeFromPickupDict(addressDict, dateScheduleDict);
    });

    return addressDict, dateScheduleDict;
}

function writeFromPickupDict(addressDict, dateScheduleDict) { // Dodanie formDict jako argumentu
    const firstRow = document.querySelectorAll('.form-section--columns > .form-section--column:first-child li');
    const secondRow = document.querySelectorAll('.form-section--columns > .form-section--column:nth-child(2) li');
    firstRow.forEach((item, index) => {
        const keys = Object.keys(addressDict);
        item.textContent = addressDict[keys[index]];

        secondRow.forEach((item, index) => {
            const keys = Object.keys(dateScheduleDict)
            item.textContent = dateScheduleDict[keys[index]];
        })
    });
}
