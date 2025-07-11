UI_PATH ?= $(CURDIR)/uiap/ui
PYUI_PATH ?= $(CURDIR)/uiap/gui
APP_PATH ?= $(CURDIR)/uiap
PYUIC_PATH ?= pyside6-uic
PYRCC_PATH ?= pyside6-rcc

UI_FILES := $(wildcard $(UI_PATH)/*.ui)
PYUI_FILES := $(patsubst $(UI_PATH)/%.ui,$(PYUI_PATH)/Ui_%.py,$(UI_FILES))

RC_FILES := $(wildcard $(UI_PATH)/*.qrc)
PYRC_FILES := $(patsubst $(UI_PATH)/%.qrc,$(PYUI_PATH)/%_rc.py,$(RC_FILES))

# %.ui -> Ui_%.py
$(PYUI_PATH)/Ui_%.py: $(UI_PATH)/%.ui
	@echo "Compiling $< -> $@"
	$(PYUIC_PATH) "$<" -o "$@"
# %.qrc -> %_rc.py
$(PYUI_PATH)/%_rc.py: $(UI_PATH)/%.qrc
	@echo "Compiling $< -> $@"
	$(PYRCC_PATH) "$<" -o "$@"

.PHONY: all
all: run

.PHONY: compile_ui
compile_ui: $(PYUI_FILES)

.PHONY: compile_rcc
compile_rcc: $(PYRC_FILES)

.PHONY: run
run: compile_ui compile_rcc
	@echo "Running..."
	uv run $(APP_PATH)/main.py

.PHONY: install
install:
#	nuitka.cmd --standalone --onefile --enable-plugin=pyside6 $(APP_PATH)/main.py
	pyinstaller --onefile --noconsole --name=uiap $(APP_PATH)/main.py

.PHONY: clean
clean:
	rm -f $(PYUI_FILES) $(PYRC_FILES)