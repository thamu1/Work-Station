import javax.mail.{Message, Session}
import javax.mail.internet.{InternetAddress, MimeMessage}
import java.util.Properties

object EmailSender extends App {

val host = "smtp.gmail.com"  // e.g., "smtp.gmail.com"
val port = "587"  // e.g., "587"
val username = "taahirimraan8601@gmail.com"
val password = "klhydsvqzntenwzz"

val to = "methamu8601@gmail.com"

// Create the email session
val properties = new Properties()
properties.put("mail.smtp.auth", "true")
properties.put("mail.smtp.starttls.enable", "true")
properties.put("mail.smtp.host", host)
properties.put("mail.smtp.port", port)

val session = Session.getInstance(properties)

val message = new MimeMessage(session)
message.setFrom(new InternetAddress(username))
message.addRecipient(Message.RecipientType.TO, new InternetAddress(to))
message.setSubject("Hi this is from Scala Man..")
message.setText("Fuck !!! this is working..")

// Send the email
val transport = session.getTransport("smtp")
transport.connect(host, username, password)
transport.sendMessage(message, message.getAllRecipients)
transport.close()

println("Email sent successfully.")
}
