using System;
using Windows.Media.Control;

// adapted from https://stackoverflow.com/questions/46777461/currently-playing-song-from-windows-10-now-playing-card
// all credits to original author

public static void PrintCurrentlyPlaying()
{
   var sessionManager = GlobalSystemMediaTransportControlsSessionManager.RequestAsync().GetAwaiter().GetResult();
   var currentSession = sessionManager.GetCurrentSession();
   var mediaProperties = currentSession.TryGetMediaPropertiesAsync().GetAwaiter().GetResult();
   Console.WriteLine($"Playing {mediaProperties.Title} by {mediaProperties.Artist}");
}