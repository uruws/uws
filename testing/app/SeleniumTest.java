import java.net.URL;
import java.util.concurrent.TimeUnit;

import org.junit.Assert;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WebDriverException;

import org.openqa.selenium.JavascriptExecutor;

import org.openqa.selenium.remote.Augmenter;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

import java.util.Date;
import java.text.SimpleDateFormat;

import org.openqa.selenium.support.ui.Select;

import io.flood.selenium.FloodSump;

import java.io.File;
import java.util.List;
import java.util.Random;

public class SeleniumTest  {

  public static void takeSnapShot(WebDriver webdriver,String fileWithPath) throws Exception{
      //Convert web driver object to TakeScreenshot
      TakesScreenshot scrShot =((TakesScreenshot)webdriver);
      //Call getScreenshotAs method to create image file
      File SrcFile=scrShot.getScreenshotAs(OutputType.FILE);
      //Move image file to new destination
      File DestFile=new File(fileWithPath);
      //Copy file at destination
      FileUtils.copyFile(SrcFile, DestFile);
  }

  public static void main(String[] args) throws Exception {

    int iterations = 0;

    /* Create a new instance of the html unit driver
       Notice that the remainder of the code relies on the interface,
       not the implementation. */
    WebDriver driver = new RemoteWebDriver(new URL("http://" + System.getenv("WEBDRIVER_HOST") + ":" + System.getenv("WEBDRIVER_PORT") + "/wd/hub"), DesiredCapabilities.chrome());
    JavascriptExecutor js = (JavascriptExecutor)driver;

    //Use an implicit wait for all object identification
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);

    /* Create a new instance of the Flood IO agent */
    FloodSump flood = new FloodSump();

    /* Inform Flood IO the test has started */
    flood.started();

    /* It's up to you to control test duration / iterations programatically. */
    while( iterations < 100 ) {
      try {

        //navigate to the home page
        flood.start_transaction("navigate login");
        driver.get("https://sarmiento.uws.talkingpts.org");
        flood.passed_transaction(driver,"navigate login");
        Thread.sleep(4000);

        //click on Accessories link
        flood.start_transaction("login demo");
        js.executeScript("Meteor.loginWithPassword('demo@lausd.org','123456');");
        driver.get("https://sarmiento.uws.talkingpts.org/schools/");
        Thread.sleep(4000);
        flood.passed_transaction(driver, "login demo");

        //click on Add to Cart link for the Beanie product
        flood.start_transaction("teacher mode");
        driver.get("https://sarmiento.uws.talkingpts.org/teachers/");
        Thread.sleep(4000);
        flood.passed_transaction(driver, "teacher mode");

        //click on View Cart
        flood.start_transaction("logout");
        js.executeScript("Meteor.logout();");
        flood.passed_transaction(driver, "logout");

        iterations++;

        /* Good idea to introduce some form of pacing / think time into your scripts */
        Thread.sleep(4000);

      } catch (WebDriverException e) {
        String[] lines = e.getMessage().split("\\r?\\n");
        System.err.println("Webdriver exception: " + lines[0]);
        flood.failed_transaction(driver);
      } catch(InterruptedException e) {
        Thread.currentThread().interrupt();
        String[] lines = e.getMessage().split("\\r?\\n");
        System.err.println("Browser terminated early: " + lines[0]);
      } catch(Exception e) {
        String[] lines = e.getMessage().split("\\r?\\n");
        System.err.println("Other exception: " + lines[0]);
      } finally {
        iterations++;
      }
    }

    driver.quit();

    /* Inform Flood IO the test has finished */
    flood.finished();
  }
}
