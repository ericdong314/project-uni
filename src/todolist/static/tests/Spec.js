describe("Todolist JavaScript", () => {
    const inputId = "id_text"
    const errorClass = "invalid-feedback"
    const inputSelector = `#${inputId}`
    const errorSelector = `.${errorClass}`
    let testDiv;
    let errorMsg;
    let textInput;

    beforeEach(() => {
        console.log("beforeEach")
        testDiv = document.createElement("div");
        testDiv.innerHTML = `  
      <form>
        <input
          id="${inputId}"
          name="text"
          class="form-control form-control-lg is-invalid"
          placeholder="Enter a to-do item"
          value="Value as submitted"
          aria-describedby="id_text_feedback"
          required
        />
        <div id="id_text_feedback" class="${errorClass}">An error message</div>
      </form>
    `;
        document.body.appendChild(testDiv);
        errorMsg = document.querySelector(errorSelector);
        textInput = document.querySelector(inputSelector);
    });

    afterEach(() => {
        testDiv.remove();
    });

    it("should have a useful html fixture", () => {
        expect(errorMsg.checkVisibility()).toBe(true);
    });

    it('should not hide error message before input', () => {
        initialize(inputSelector)
        expect(errorMsg.checkVisibility()).toBe(true);
    });

    it("should hide error message on input", () => {
        initialize(inputSelector);
        textInput.dispatchEvent(new InputEvent("input"));
        expect(errorMsg.checkVisibility()).toBe(false);
    });

    it('should hide error message on clicking', () => {
        initialize(inputSelector);
        textInput.dispatchEvent(new MouseEvent("click"));
        expect(errorMsg.checkVisibility()).toBe(false)
    });
});