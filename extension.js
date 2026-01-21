const vscode = require('vscode');
const layout = require('./jis_layout.json');

// JIS配列の「Shiftなし」と「Shiftあり」の対応表
const jisShiftMap = {
    '1': '!', '2': '"', '3': '#', '4': '$', '5': '%', 
    '6': '&', '7': "'", '8': '(', '9': ')', '0': '', // 0のShiftは特殊なので除外またはそのまま
    '-': '=', '^': '~', '¥': '|', '@': '`', '[': '{', 
    ';': '+', ':': '*', ']': '}', ',': '<', '.': '>', 
    '/': '?', '\\': '_', 'IntlRo': '_' // アンダースコアの対応
};

// 逆引き用（Shiftされた文字から元のキーを探す）
const reverseJisMap = {};
Object.keys(jisShiftMap).forEach(key => {
    reverseJisMap[jisShiftMap[key]] = key;
});

function activate(context) {
    console.log('Custom JIS Layout (Fixed) is now active!');

    let typeCommand = vscode.commands.registerCommand('type', (args) => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }

        const inputChar = args.text;
        const mappedChar = mapCharacter(inputChar);

        editor.edit(editBuilder => {
            editor.selections.forEach(selection => {
                if (!selection.isEmpty) {
                    editBuilder.replace(selection, mappedChar);
                } else {
                    editBuilder.insert(selection.active, mappedChar);
                }
            });
        });
    });

    context.subscriptions.push(typeCommand);
}

function mapCharacter(inputChar) {
    // 1. 入力がShiftされているか、元のキーは何かを判定
    let baseKey = inputChar;
    let isShifted = false;

    // アルファベットの場合
    if (inputChar.match(/[A-Z]/)) {
        isShifted = true;
        baseKey = inputChar;
    } else if (inputChar.match(/[a-z]/)) {
        isShifted = false;
        baseKey = inputChar.toUpperCase();
    } 
    // 記号の場合（Shiftされた記号かチェック）
    else if (reverseJisMap[inputChar]) {
        isShifted = true;
        baseKey = reverseJisMap[inputChar];
    }
    // Shiftされていない記号の場合
    else {
        isShifted = false;
        baseKey = inputChar;
    }

    // 2. JSONからマッピング先を取得
    // JSONには "Q", "1", "-" のようにベースキーで定義されている前提
    if (!layout.hasOwnProperty(baseKey)) {
        return inputChar; // 定義がなければそのまま
    }

    const targetBase = layout[baseKey];

    // 値が特殊キー（Escなど）の場合はそのまま返す
    if (targetBase.length > 1) {
        return targetBase; 
    }

    // 3. マッピング先の文字に対して、Shift状態を適用して返す
    if (isShifted) {
        // Shiftありの場合
        
        // ターゲットがアルファベットなら大文字
        if (targetBase.match(/[A-Z]/)) {
            return targetBase;
        }
        // ターゲットが記号なら、その記号のShift版を返す
        if (jisShiftMap[targetBase]) {
            return jisShiftMap[targetBase];
        }
        // Shift版の定義がない記号ならそのまま
        return targetBase;

    } else {
        // Shiftなしの場合

        // ターゲットがアルファベットなら小文字にする（これが「Shiftなしなら大文字」の修正）
        if (targetBase.match(/[A-Z]/)) {
            return targetBase.toLowerCase();
        }
        // 記号ならそのまま
        return targetBase;
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};